#!/usr/bin/env python3
"""
Calibración automatizada: corre cada caso de prueba N veces contra el
pipeline real (Doppler -> Anthropic) y reporta variación de puntaje y
banderas. Reemplaza "corrí un caso a mano y lo leí una vez" por un número
medible y repetible.

Uso:
    python calibrar.py [repeticiones]   (default: 3)

Requiere DOPPLER_TOKEN configurado (igual que la app).
"""
import statistics
import sys
import time
from pathlib import Path

SERVER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(SERVER_DIR))
try:
    sys.stdout.reconfigure(encoding="utf-8")
except AttributeError:
    pass

import anthropic_client
import corrector
import doppler_client
import validador

HERRAMIENTAS_DIR = SERVER_DIR.parent
CORRECTOR_DIR = HERRAMIENTAS_DIR.parent          # parcial-agente-evaluador/
DATA_DIR = HERRAMIENTAS_DIR / "data"
CASOS_EXTRA = HERRAMIENTAS_DIR / "casos-extra"    # casos de testing nuestros, no la entrega oficial

REPETICIONES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
FILTRO = sys.argv[2].split(",") if len(sys.argv) > 2 else None  # ej: "excelente,tramposo"

CASOS = [
    {"nombre": "excelente", "ruta": CORRECTOR_DIR / "casos" / "excelente",
     "fecha": "2026-09-02", "banda": (85, 100), "bandera_esperada": None},
    {"nombre": "flojo", "ruta": CORRECTOR_DIR / "casos" / "flojo",
     "fecha": "2026-09-02", "banda": (40, 54), "bandera_esperada": None},
    {"nombre": "tramposo", "ruta": CORRECTOR_DIR / "casos" / "tramposo",
     "fecha": "2026-09-02", "banda": (0, 45), "bandera_esperada": "B4"},
    {"nombre": "inconsistente (nuevo — prueba B6)", "ruta": CASOS_EXTRA / "inconsistente",
     "fecha": "2026-09-06", "banda": (50, 95), "bandera_esperada": "B6"},
    {"nombre": "oculto (nuevo — prueba B4 mecánico)", "ruta": CASOS_EXTRA / "oculto",
     "fecha": "2026-09-06", "banda": (0, 100), "bandera_esperada": "B4"},
]


def main():
    cf = corrector.cargar_archivos_corrector(CORRECTOR_DIR)
    if not cf:
        print(f"ERROR: no se encontró rubrica.md / agente/system_prompt.md en {CORRECTOR_DIR}")
        sys.exit(1)
    try:
        creds = doppler_client.get_credentials(DATA_DIR)
    except doppler_client.DopplerError as e:
        print(f"ERROR Doppler: {e}")
        sys.exit(1)

    print(f"Modelo: {creds['model']} · Repeticiones por caso: {REPETICIONES}\n")

    resumen = []
    casos_a_correr = [c for c in CASOS if not FILTRO or any(f in c["nombre"] for f in FILTRO)]
    for caso in casos_a_correr:
        print(f"=== {caso['nombre']} ({REPETICIONES} corridas, fecha {caso['fecha']}) ===")
        try:
            dump = corrector.construir_dump(str(caso["ruta"]), CORRECTOR_DIR)
        except corrector.RutaInvalida as e:
            print(f"  ERROR: {e}\n")
            continue

        notas, banderas_vistas, fuera_de_banda, truncadas, invalidas = [], set(), [], 0, 0
        for i in range(REPETICIONES):
            cached_prefix, user_text = corrector.construir_prompts(caso["nombre"], caso["fecha"], cf["rubrica"], dump)
            t0 = time.time()
            try:
                r = anthropic_client.call(creds["apiKey"], creds["model"], cf["systemPrompt"], user_text, cached_prefix=cached_prefix)
            except anthropic_client.AnthropicError as e:
                print(f"  corrida {i+1}: ERROR DE API — {e}")
                continue
            dt = time.time() - t0
            v = validador.validar(r["text"])
            total = v["parsed"]["total"]
            bs = v["parsed"]["banderas"]
            banderas_vistas.update(bs)
            if total is not None:
                notas.append(total)
            if r["truncado"]:
                truncadas += 1
            if v["veredicto"] == "bad":
                invalidas += 1
            fuera = total is not None and not (caso["banda"][0] <= total <= caso["banda"][1])
            if fuera:
                fuera_de_banda.append(total)
            marca = []
            if r["truncado"]:
                marca.append("TRUNCADA")
            if v["veredicto"] == "bad":
                marca.append("FORMATO INVALIDO")
            if fuera:
                marca.append("FUERA DE BANDA")
            u = r["usage"]
            print(
                f"  corrida {i+1}: {total}/100 · banderas {bs or ['ninguna']} · {dt:.1f}s · "
                f"tokens in={u['entrada']} (cache={u['cacheLeido']}) out={u['salida']}"
                + (f"  ⚠ {', '.join(marca)}" if marca else "")
            )

        if notas:
            spread = max(notas) - min(notas)
            print(
                f"  -> min={min(notas)} max={max(notas)} promedio={statistics.mean(notas):.1f} "
                f"spread={spread} banderas_vistas={sorted(banderas_vistas)}"
            )
            if caso["bandera_esperada"] and caso["bandera_esperada"] not in banderas_vistas:
                print(f"  ⚠⚠ Se esperaba ver {caso['bandera_esperada']} en alguna corrida y NO apareció en ninguna")
        else:
            spread = None
            print("  -> ninguna corrida devolvió un total válido")
        print()
        resumen.append({
            "caso": caso["nombre"], "notas": notas, "spread": spread,
            "banderas": sorted(banderas_vistas), "truncadas": truncadas, "invalidas": invalidas,
            "fuera_de_banda": fuera_de_banda,
        })

    print("=" * 70)
    print("RESUMEN FINAL")
    print("=" * 70)
    for r in resumen:
        alerta = " ⚠" if (r["fuera_de_banda"] or r["truncadas"] or r["invalidas"]) else ""
        print(f"{r['caso']}: notas={r['notas']} spread={r['spread']} banderas={r['banderas']}"
              f" truncadas={r['truncadas']} invalidas={r['invalidas']}{alerta}")


if __name__ == "__main__":
    main()

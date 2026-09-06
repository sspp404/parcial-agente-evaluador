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
import os
import statistics
import sys
import time
from datetime import datetime
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
# Los casos extra viven en la raíz del repositorio y SÍ se versionan: sin la
# salida cruda y sin el caso navegable, una ronda de calibración es una
# afirmación sin respaldo — la bandera B1 que este mismo agente le aplica a los
# demás. Antes esta carpeta estaba en .gitignore.
CASOS_EXTRA = CORRECTOR_DIR / "casos-extra"
CORRECCIONES_DIR = CORRECTOR_DIR / "correcciones"

REPETICIONES = int(sys.argv[1]) if len(sys.argv) > 1 else 3
FILTRO = sys.argv[2].split(",") if len(sys.argv) > 2 else None  # ej: "excelente,tramposo"

CASOS = [
    {"nombre": "excelente", "ruta": CORRECTOR_DIR / "casos" / "excelente",
     "fecha": "2026-09-02", "banda": (85, 100), "banderas_esperadas": ["B1", "B2a"]},
    {"nombre": "flojo", "ruta": CORRECTOR_DIR / "casos" / "flojo",
     "fecha": "2026-09-02", "banda": (40, 54), "banderas_esperadas": ["B1"]},
    {"nombre": "tramposo", "ruta": CORRECTOR_DIR / "casos" / "tramposo",
     "fecha": "2026-09-02", "banda": (0, 45), "banderas_esperadas": ["B1", "B2b", "B3", "B4"]},
    # Casos extra: cubren las banderas que los tres oficiales no ejercitan y la
    # zona intermedia de la rúbrica, donde van a caer la mayoría de los trabajos
    # reales de la prueba de fuego. Nombres sin paréntesis: se usan como nombre
    # de archivo al guardar la salida cruda.
    {"nombre": "inconsistente", "ruta": CASOS_EXTRA / "inconsistente",
     "fecha": "2026-09-06", "banda": (55, 85), "banderas_esperadas": ["B6"]},
    {"nombre": "oculto", "ruta": CASOS_EXTRA / "oculto",
     "fecha": "2026-09-06", "banda": (40, 75), "banderas_esperadas": ["B4"]},
    {"nombre": "intermedio", "ruta": CASOS_EXTRA / "intermedio",
     "fecha": "2026-09-06", "banda": (68, 84), "banderas_esperadas": []},
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
    fallas = []
    guardadas = []
    etiqueta = datetime.now().strftime("%Y%m%d-%H%M")
    salida_dir = CORRECCIONES_DIR / f"corrida_{etiqueta}"
    salida_dir.mkdir(parents=True, exist_ok=True)
    print(f"Salidas crudas -> {os.path.relpath(salida_dir, CORRECTOR_DIR)}/\n")
    casos_a_correr = [c for c in CASOS if not FILTRO or any(f in c["nombre"] for f in FILTRO)]
    for caso in casos_a_correr:
        print(f"=== {caso['nombre']} ({REPETICIONES} corridas, fecha {caso['fecha']}) ===")
        try:
            dump = corrector.construir_dump(str(caso["ruta"]), CORRECTOR_DIR)
        except corrector.RutaInvalida as e:
            # Un caso declarado cuya carpeta no está es una falla, no un aviso.
            # Es exactamente lo que pasaba con casos-extra/: calibracion.md
            # reportaba resultados de un caso que no estaba en el repositorio.
            print(f"  ✗ FALLA · carpeta ausente: {e}\n")
            fallas.append(f"{caso['nombre']}: la carpeta del caso no existe ({caso['ruta']})")
            continue

        notas, banderas_vistas, fuera_de_banda, truncadas, invalidas = [], set(), [], 0, 0
        for i in range(REPETICIONES):
            cached_prefix, user_text = corrector.construir_prompts(caso["nombre"], caso["fecha"], cf["rubrica"], dump)
            t0 = time.time()
            try:
                r = anthropic_client.call(creds["apiKey"], creds["model"], cf["systemPrompt"], user_text, cached_prefix=cached_prefix)
            except anthropic_client.AnthropicError as e:
                # Antes esto solo imprimía y seguía. Si TODAS las corridas de un
                # caso morían por un 429, el chequeo de banderas —que vive dentro
                # de `if notas:`— no corría, y el script terminaba con
                # "✓ Calibración OK" y código 0. Una calibración que no midió
                # nada no puede reportarse como una que pasó.
                print(f"  corrida {i+1}: ✗ ERROR DE API — {e}")
                fallas.append(f"{caso['nombre']}: corrida {i+1} falló por error de API ({e})")
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

            # La salida cruda se guarda SIEMPRE, sin editar. Las rondas 3 y 4 se
            # corrieron con este script cuando solo imprimía: 22 corridas descritas
            # en calibracion.md y cero archivos que las respalden. Una calibración
            # cuya evidencia vive en una terminal que ya se cerró no es evidencia.
            slug = "".join(c if c.isalnum() or c in "-_" else "_" for c in caso["nombre"])
            destino = salida_dir / f"{slug}_{i+1}.md"
            destino.write_text(
                f"<!-- generado por calibrar.py · caso={caso['nombre']} · corrida={i+1}/{REPETICIONES}\n"
                f"     fecha de corrección={caso['fecha']} · modelo={creds['model']}\n"
                f"     tokens in={u['entrada']} (cache={u['cacheLeido']}) out={u['salida']} · {dt:.1f}s\n"
                f"     stop_reason={r.get('stop_reason')} · veredicto de formato={v['veredicto']}\n"
                f"     SALIDA SIN EDITAR -->\n\n{r['text']}\n",
                encoding="utf-8",
            )
            guardadas.append(destino)

        if notas and len(notas) < REPETICIONES:
            fallas.append(
                f"{caso['nombre']}: solo {len(notas)} de {REPETICIONES} corridas dieron un total "
                f"válido — el spread reportado no es comparable con el de los otros casos"
            )
        if notas:
            spread = max(notas) - min(notas)
            print(
                f"  -> min={min(notas)} max={max(notas)} promedio={statistics.mean(notas):.1f} "
                f"spread={spread} banderas_vistas={sorted(banderas_vistas)}"
            )
            # Antes solo el caso tramposo declaraba una bandera esperada, y el
            # chequeo era un print: una calibración podía "pasar" con la mitad
            # de las banderas perdidas. Es el mismo modo de falla que la Ronda 4
            # documenta —un validador con un bug reporta falsos negativos con la
            # misma confianza que un resultado real—, así que ahora se verifican
            # todas las que el repo declara y la corrida se marca como fallida.
            faltantes = [b for b in caso.get("banderas_esperadas") or [] if b not in banderas_vistas]
            if faltantes:
                fallas.append(f"{caso['nombre']}: no apareció {', '.join(faltantes)} en ninguna corrida")
                print(f"  ✗ FALLA · se esperaban {caso['banderas_esperadas']} y faltaron: {', '.join(faltantes)}")
        else:
            spread = None
            print("  -> ✗ ninguna corrida devolvió un total válido")
            fallas.append(f"{caso['nombre']}: ninguna de las {REPETICIONES} corridas devolvió un total válido")
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

    print(f"\n{len(guardadas)} salida(s) cruda(s) guardada(s) en {os.path.relpath(salida_dir, CORRECTOR_DIR)}/")

    if fallas:
        print("\n✗ La calibración NO pasó:")
        for f in fallas:
            print(f"   - {f}")
        return 1
    if not guardadas:
        print("\n✗ No se guardó ninguna salida cruda: no hay evidencia de que esta calibración haya corrido.")
        return 1
    print(f"\n✓ Calibración OK: {len(guardadas)} corridas guardadas y todas las banderas esperadas aparecieron.")
    return 0


if __name__ == "__main__":
    sys.exit(main() or 0)

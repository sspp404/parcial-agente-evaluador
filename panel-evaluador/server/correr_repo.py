#!/usr/bin/env python3
"""
Corrige UN repositorio real, traído por URL de GitHub, y guarda la salida
cruda en `correcciones/`.

`calibrar.py` corre los casos de prueba: carpetas que escribimos nosotros,
en disco, con la estructura que nosotros decidimos. Este script corre lo
otro — un repositorio ajeno, clonado de GitHub, con la forma que tenga. Es
el mismo camino que va a recorrer la prueba de fuego, y el único que
demuestra lo que el parcial pide en su segundo criterio: que el corrector
"corre sobre un repo real y devuelve el formato completo".

Uso:
    python3 correr_repo.py <url-o-ruta> [--nombre X] [--fecha AAAA-MM-DD] [--n 1]

Ejemplos:
    python3 correr_repo.py https://github.com/MoonquantCap/agentes-ia-ucema
    python3 correr_repo.py ../otro-trabajo --nombre "trabajo de prueba" --n 2

Credenciales: DOPPLER_TOKEN o ANTHROPIC_API_KEY (ver panel-evaluador/README.md).
El clon es COMPLETO a propósito: `--depth 1` deja un solo commit, un solo
autor y cero días de spread — justo la forma que la bandera B6 denuncia.
"""
import argparse
import os
import shutil
import subprocess
import sys
import tempfile
import time
from datetime import date, datetime
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

DATA_DIR = SERVER_DIR.parent / "data"
CORRECTOR_DIR = SERVER_DIR.parent.parent          # parcial-agente-evaluador/
CORRECCIONES_DIR = CORRECTOR_DIR / "correcciones"

# claude-sonnet-5, USD por millón de tokens. Si cambia el modelo, cambian acá.
PRECIO_ENTRADA, PRECIO_SALIDA, PRECIO_CACHE_LEIDO = 2.00, 10.00, 0.20


def es_url(arg: str) -> bool:
    return arg.startswith(("http://", "https://", "git@"))


def slug(texto: str) -> str:
    return "".join(c if c.isalnum() or c in "-_" else "_" for c in texto)[:60]


def clonar(url: str, destino: Path) -> None:
    print(f"Clonando {url} (historial completo)…")
    proc = subprocess.run(
        ["git", "clone", "--", url, str(destino)],
        capture_output=True, text=True, timeout=300,
    )
    if proc.returncode != 0:
        raise SystemExit(f"✗ git clone falló: {proc.stderr.strip()[-500:]}")


def main() -> int:
    ap = argparse.ArgumentParser(description="Corrige un repositorio real con el agente evaluador.")
    ap.add_argument("repo", help="URL de GitHub o ruta local del repositorio a corregir")
    ap.add_argument("--nombre", help="cómo identificar el trabajo en la salida (default: nombre del repo)")
    ap.add_argument("--fecha", default=date.today().isoformat(), help="fecha de corrección (default: hoy)")
    ap.add_argument("--n", type=int, default=1, help="cuántas veces correrlo (default: 1)")
    args = ap.parse_args()

    cf = corrector.cargar_archivos_corrector(CORRECTOR_DIR)
    if not cf:
        print(f"ERROR: no se encontró rubrica.md / agente/system_prompt.md en {CORRECTOR_DIR}")
        return 1
    try:
        creds = doppler_client.get_credentials(DATA_DIR)
    except doppler_client.DopplerError as e:
        print(f"ERROR de credenciales: {e}")
        return 1

    temporal = None
    if es_url(args.repo):
        temporal = Path(tempfile.mkdtemp(prefix="repo-real-"))
        ruta = temporal / "repo"
        clonar(args.repo, ruta)
        nombre = args.nombre or args.repo.rstrip("/").split("/")[-1].removesuffix(".git")
    else:
        ruta = Path(args.repo).expanduser().resolve()
        nombre = args.nombre or ruta.name

    try:
        try:
            dump = corrector.construir_dump(str(ruta), CORRECTOR_DIR)
        except corrector.RutaInvalida as e:
            print(f"✗ {e}")
            return 1

        print(f"\nRepositorio: {nombre}")
        print(f"Modelo: {creds['model']} · fecha de corrección: {args.fecha}")
        print(f"Archivos en el repo: {dump['totalArchivos']} · contenido enviado: {dump['count']}")
        if dump["raizEntrega"]:
            print(f"Raíz de la entrega detectada: {dump['raizEntrega']}/")
        if dump["alertasSeguridad"]:
            print(f"Alertas del escaneo forense: {len(dump['alertasSeguridad'])}")
        gl = dump.get("gitLog")
        if gl:
            print(f"git log: {gl['commits']} commits · {len(gl['autores'])} autor(es) · "
                  f"{gl['primerCommit'][:10]} → {gl['ultimoCommit'][:10]} "
                  f"({gl['diasDeSpread']} días de spread)")
        else:
            print("git log: no disponible (sin .git, o clon superficial)")
        # Un repositorio sin NADA de la estructura obligatoria es un resultado
        # válido y esperable (el corrector debe puntuar bajo, con evidencia,
        # sin caerse) — pero conviene que quien corre el script lo sepa antes
        # de gastar la llamada, no después.
        if dump["count"] == 0:
            print("\n⚠ Este repositorio no tiene ninguno de los archivos que el contrato pide leer\n"
                  "  (README.md, DECISIONES.md, prompts/, corridas/). El corrector va a recibir el\n"
                  "  listado completo y ningún contenido: es un caso legítimo de nota baja, no un error.")

        etiqueta = datetime.now().strftime("%Y%m%d-%H%M")
        salida_dir = CORRECCIONES_DIR / f"repo-real_{slug(nombre)}_{etiqueta}"
        guardadas = []

        for i in range(args.n):
            cached_prefix, user_text = corrector.construir_prompts(nombre, args.fecha, cf["rubrica"], dump)
            t0 = time.time()
            try:
                r = anthropic_client.call(
                    creds["apiKey"], creds["model"], cf["systemPrompt"], user_text,
                    cached_prefix=cached_prefix,
                )
            except anthropic_client.AnthropicError as e:
                print(f"  corrida {i+1}: ✗ ERROR DE API — {e}")
                continue
            dt = time.time() - t0
            v = validador.validar(r["text"], dump_count=dump["count"])
            u = r["usage"]
            costo = (u["entrada"] * PRECIO_ENTRADA + u["salida"] * PRECIO_SALIDA
                     + u["cacheLeido"] * PRECIO_CACHE_LEIDO) / 1_000_000
            marca = []
            if r["truncado"]:
                marca.append("TRUNCADA")
            if v["veredicto"] == "bad":
                marca.append("FORMATO INVALIDO")
            print(
                f"  corrida {i+1}: {v['parsed']['total']}/100 · "
                f"banderas {v['parsed']['banderas'] or ['ninguna']} · {dt:.1f}s · "
                f"tokens in={u['entrada']} (cache={u['cacheLeido']}) out={u['salida']} · "
                f"USD {costo:.4f}"
                + (f"  ⚠ {', '.join(marca)}" if marca else "")
            )

            salida_dir.mkdir(parents=True, exist_ok=True)
            destino = salida_dir / f"{slug(nombre)}_{i+1}.md"
            destino.write_text(
                f"<!-- generado por correr_repo.py · repo={args.repo} · corrida={i+1}/{args.n}\n"
                f"     fecha de corrección={args.fecha} · modelo={creds['model']}\n"
                f"     archivos en el repo={dump['totalArchivos']} · contenido enviado={dump['count']}\n"
                f"     tokens in={u['entrada']} (cache={u['cacheLeido']}) out={u['salida']} · {dt:.1f}s\n"
                f"     costo estimado=USD {costo:.4f}\n"
                f"     stop_reason={r.get('stop_reason')} · veredicto de formato={v['veredicto']}\n"
                f"     SALIDA SIN EDITAR -->\n\n{r['text']}\n",
                encoding="utf-8",
            )
            guardadas.append(destino)

        if not guardadas:
            print("\n✗ No se guardó ninguna salida: la corrida no dejó evidencia.")
            return 1
        print(f"\n✓ {len(guardadas)} salida(s) cruda(s) en "
              f"{os.path.relpath(salida_dir, CORRECTOR_DIR)}/")
        return 0
    finally:
        if temporal:
            shutil.rmtree(temporal, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())

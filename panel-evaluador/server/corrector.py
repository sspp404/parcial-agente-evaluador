"""
Lectura de carpetas locales: arma el "dump" del repositorio a evaluar y lee
el corrector (rubrica.md + agente/system_prompt.md) directo del disco.

A diferencia de la versión anterior (input type=file en el navegador), acá el
backend tiene acceso directo al sistema de archivos: no hace falta volver a
elegir carpetas en cada corrida, alcanza con la ruta ya guardada del proyecto.
"""
import os
from pathlib import Path

import forense


class RutaInvalida(RuntimeError):
    pass


EXT_LEGIBLES = {".md", ".mdx", ".txt", ".json", ".yml", ".yaml", ".py", ".js", ".ts", ".csv", ".mjs", ".cjs"}
EXCLUDE_DIRS = {".git", "node_modules", "__pycache__", "panel-evaluador", "data", ".venv", "venv"}
MAX_POR_ARCHIVO = 150_000   # caracteres
MAX_DUMP_TOTAL = 400_000    # caracteres

# El contrato del corrector (agente/system_prompt.md) es explícito: solo tiene
# que leer README.md, DECISIONES.md, y todo lo que haya en prompts/ y corridas/.
# Leer más que eso no lo pide nadie y solo infla el costo de cada corrida —
# por eso el contenido se limita a estas rutas, aunque el LISTADO de archivos
# (más abajo) sigue mostrando el repositorio completo.
ARCHIVOS_RAIZ_REQUERIDOS = {"readme.md", "decisiones.md"}
CARPETAS_REQUERIDAS = {"prompts", "corridas"}


def _es_contenido_requerido(rel_posix: str) -> bool:
    partes = rel_posix.lower().split("/")
    if len(partes) == 1:
        return partes[0] in ARCHIVOS_RAIZ_REQUERIDOS
    return partes[0] in CARPETAS_REQUERIDAS


def _iter_todos_los_archivos(root: Path):
    """Todo el repositorio, sin filtrar por extensión — para el listado."""
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not d.startswith(".")]
        for fn in sorted(filenames):
            yield Path(dirpath) / fn


def _iter_archivos(root: Path):
    """Archivos legibles Y relevantes (lo usa verificar_carpeta, el chequeo
    previo que ve el usuario antes de correr). Antes contaba cualquier archivo
    legible del repositorio entero, así que una carpeta con código fuente pero
    sin README.md/DECISIONES.md/prompts/corridas mostraba "✓ N archivos
    legibles" y después construir_dump igual devolvía count=0 (la carpeta
    "no tiene archivos legibles") al correr de verdad — el chequeo tiene que
    mirar lo mismo que se va a enviar, no una definición más laxa."""
    for p in _iter_todos_los_archivos(root):
        if p.suffix.lower() in EXT_LEGIBLES:
            rel = p.relative_to(root).as_posix()
            if _es_contenido_requerido(rel):
                yield p


def _resolver(ruta: str, base: Path) -> Path:
    """Una ruta relativa se resuelve contra `base` (la carpeta del corrector),
    no contra el directorio de trabajo del proceso — que puede ser cualquier
    cosa según desde dónde se haya lanzado el servidor."""
    p = Path(ruta).expanduser()
    if not p.is_absolute():
        p = base / p
    return p.resolve()


def construir_dump(ruta: str, base: Path) -> dict:
    """Arma dos cosas por separado, para no pagar tokens de más:

    - `listado`: las rutas de TODOS los archivos del repositorio (barato: son
      solo nombres). Cumple el paso 1 del contrato ("listar todos los
      archivos") y le sirve al corrector para juzgar D3 (formato) sin
      necesidad de leer el contenido de cada uno.
    - `text`: el CONTENIDO completo, pero solo de README.md, DECISIONES.md,
      prompts/ y corridas/ — que es todo lo que el contrato (paso 2) pide
      leer. Un repo con código fuente propio, node_modules, assets, etc. ya
      no se manda entero: eso antes se pagaba como tokens de entrada sin que
      nadie lo hubiera pedido.
    """
    root = _resolver(ruta, base)
    if not root.exists() or not root.is_dir():
        raise RutaInvalida(f"La carpeta no existe: {root}")

    todos = [p.relative_to(root).as_posix() for p in _iter_todos_los_archivos(root)]
    listado = "\n".join(todos)

    partes = []
    total = 0
    count = 0
    omitidos = []
    cortado = False
    alertas_seguridad = []
    for rel in todos:
        if not _es_contenido_requerido(rel):
            continue
        p = root / rel
        if p.suffix.lower() not in EXT_LEGIBLES:
            omitidos.append(f"{rel} (extensión no legible, se omite el contenido)")
            continue
        try:
            size = p.stat().st_size
        except OSError:
            continue
        if size > MAX_POR_ARCHIVO:
            omitidos.append(f"{rel} ({round(size / 1000)} KB, muy grande)")
            continue
        try:
            content = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        alertas_seguridad.extend(forense.escanear_texto(content, rel))
        if total + len(content) > MAX_DUMP_TOTAL:
            cortado = True
            break
        partes.append(f"### Archivo: {rel}\n```\n{content}\n```")
        total += len(content)
        count += 1

    return {
        "listado": listado,
        "totalArchivos": len(todos),
        "text": "\n\n".join(partes),
        "count": count,
        "totalChars": total,
        "cortado": cortado,
        "omitidos": omitidos,
        "root": str(root),
        "alertasSeguridad": alertas_seguridad,
        "gitLog": forense.leer_historial_git(root),
    }


def verificar_carpeta(ruta: str, base: Path) -> dict:
    """Vista previa liviana para el botón "Verificar carpeta" del frontend:
    no arma el dump completo, solo cuenta y confirma que existe."""
    root = _resolver(ruta, base)
    if not root.exists():
        return {"existe": False, "esCarpeta": False, "archivos": 0}
    if not root.is_dir():
        return {"existe": True, "esCarpeta": False, "archivos": 0}
    n = sum(1 for _ in _iter_archivos(root))
    return {"existe": True, "esCarpeta": True, "archivos": n, "root": str(root)}


def listar_subcarpetas(ruta: str | None, base: Path) -> dict:
    """Para el explorador de carpetas del frontend (modo 'ZIP / carpeta
    local'): un navegador no puede darle al backend una ruta absoluta de una
    carpeta elegida por el usuario (por seguridad del propio navegador), así
    que en vez de eso el backend expone sus propias carpetas para navegar."""
    root = _resolver(ruta, base) if ruta else base.parent
    if not root.exists() or not root.is_dir():
        root = base.parent  # ruta rota: volvemos a un punto de partida seguro

    try:
        entradas = sorted(
            (d for d in root.iterdir() if d.is_dir() and not d.name.startswith(".") and d.name not in EXCLUDE_DIRS),
            key=lambda d: d.name.lower(),
        )
    except OSError:
        entradas = []

    return {
        "path": str(root),
        "parent": str(root.parent) if root.parent != root else None,
        "carpetas": [{"nombre": d.name, "path": str(d)} for d in entradas],
    }


def construir_prompts(proyecto_nombre: str, fecha: str, rubrica_texto: str, dump: dict) -> tuple[str, str]:
    """Arma (cached_prefix, user_text) — el mismo texto exacto que arma la
    app real (app.py) para una corrida, factorizado acá para que el script
    de calibración (calibrar.py) use la lógica idéntica, no una copia que se
    pueda desincronizar con el tiempo."""
    cached_prefix = f"=== rubrica.md (tu única vara de corrección) ===\n{rubrica_texto}"

    bloque_forense = forense.construir_bloque_prompt(dump["alertasSeguridad"], dump["gitLog"])

    user_text = (
        f"Repositorio evaluado: {proyecto_nombre}\n"
        f"Fecha de corrección: {fecha}\n"
        f"{bloque_forense}\n"
        f"=== Listado completo de archivos del repositorio ({dump['totalArchivos']}) ===\n"
        f"{dump['listado']}\n\n"
        f"=== Contenido de README.md, DECISIONES.md, prompts/ y corridas/ ===\n"
        f"Ya fue leído en tu lugar por la herramienta leer_repo — es todo lo que tu contrato "
        f"pide leer. El resto de los archivos del listado de arriba existe pero no hace falta "
        f"su contenido para corregir. A continuación el contenido completo de {dump['count']} "
        f"archivo(s)"
        f"{' (se recortó por tamaño, puede faltar contenido)' if dump['cortado'] else ''}:\n\n"
        f"{dump['text']}\n\n"
        f"=== Tarea ===\n"
        f"Corregí este trabajo aplicando la rúbrica completa. Devolvé la corrección en el "
        f"formato fijo definido en tu system prompt, sin comentarios por fuera de ese formato."
    )
    return cached_prefix, user_text


def cargar_archivos_corrector(corrector_dir: Path) -> dict | None:
    rubrica_path = corrector_dir / "rubrica.md"
    system_path = corrector_dir / "agente" / "system_prompt.md"
    if not rubrica_path.exists() or not system_path.exists():
        return None
    return {
        "rubrica": rubrica_path.read_text(encoding="utf-8"),
        "systemPrompt": system_path.read_text(encoding="utf-8"),
    }

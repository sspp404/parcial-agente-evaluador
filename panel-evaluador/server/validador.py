"""
Parser y validador de la salida del agente corrector — puerto a Python del
mismo chequeo que tenía la versión anterior en JavaScript, ahora como única
fuente de verdad (antes vivía duplicado si el frontend también validaba).
"""
import re

NIVELES = {30: [30, 24, 18, 10, 0], 25: [25, 20, 14, 7, 0], 15: [15, 12, 8, 4, 0]}
DIM_LABEL = {
    1: "Sistema completo",
    2: "Proceso documentado",
    3: "Formato y reproducibilidad",
    4: "Análisis económico",
    5: "Gobierno y riesgo",
}

_RE_ARCHIVOS_LEIDOS = re.compile(r"Archivos\s+le[íi]dos:?\s*\**\s*(\d+)", re.IGNORECASE)
_RE_DIM_SCORE = re.compile(r"(\d+)\s*/\s*(30|25|15)\b")
_RE_DIM_NUM = re.compile(r"(\d)\s*[·.\-]")
_RE_TOTAL = re.compile(r"Puntaje\s+total:?\s*\**\s*(\d+)\s*/\s*100", re.IGNORECASE)
# Anclado a comienzo de línea: sin ^ , una justificación que mencione
# "la sección ## Banderas de integridad" enganchaba ahí y el parser leía un
# bloque vacío, reportando "ninguna bandera" con las banderas reales más abajo.
_RE_BANDERAS_HEADER = re.compile(r"^##\s*Banderas", re.IGNORECASE | re.MULTILINE)
_RE_FENCE = re.compile(r"```.*?```", re.DOTALL)
_RE_NEXT_HEADER = re.compile(r"\n##\s")
# Separadores admitidos después del código de bandera: el modelo alterna entre
# medio punto, dos puntos, guion corto, guion largo y raya. Anclarse a uno solo
# produce falsos negativos silenciosos — exactamente el bug de la Ronda 4, donde
# el regex conocía B1..B5 y descartaba cada B6 sin avisar (ver calibracion.md).
_RE_BANDERA_ITEM = re.compile(
    r"^\s*[-*]?\s*(B(?:2a|2b|1|2|3|4|5|6))\b\s*[·:.\-\u2010-\u2015]", re.MULTILINE
)


def _limpiar_markdown(texto: str) -> str:
    """Saca el énfasis y los backticks antes de aplicar los regex de extracción.

    El contrato pide un formato fijo, pero el modelo lo decora: escribe
    `**24**/30`, `` `B6` `` o `**B2b** —`. El parser no puede depender de que
    no lo haga: un puntaje que no matchea se cuenta como dimensión faltante y
    una bandera que no matchea desaparece del informe con la misma confianza
    con la que se reporta una real."""
    return texto.replace("**", "").replace("__", "").replace("`", "")


def _sin_bloques_de_codigo(texto: str) -> str:
    """Los bloques ``` del informe suelen citar el contrato o el repo evaluado.
    Si no se sacan antes de buscar encabezados, un trabajo que incluya en su
    README un "## Banderas de integridad" de ejemplo secuestra el parser."""
    return _RE_FENCE.sub(lambda m: "\n" * m.group(0).count("\n"), texto)
_RE_NINGUNA_BANDERA = re.compile(r"ninguna\s+bandera", re.IGNORECASE)
_RE_SUGERENCIA = re.compile(r"##\s*Sugerencia", re.IGNORECASE)
_RE_RUTA = re.compile(r"([\w\-./]+\.(md|txt|json|csv|ya?ml|py|js))|((prompts|corridas|casos|agente)/)", re.IGNORECASE)


def parse_correccion(texto: str) -> dict:
    out = {
        "archivosLeidos": None,
        "dims": [],
        "total": None,
        "banderas": [],
        "tieneSugerencia": False,
        "sinSeccionBanderas": False,
        "ningunaBandera": False,
        "raw": texto,
    }

    texto_limpio = _limpiar_markdown(texto)

    m = _RE_ARCHIVOS_LEIDOS.search(texto_limpio)
    out["archivosLeidos"] = int(m.group(1)) if m else None

    filas = [l for l in texto.split("\n") if l.strip().startswith("|")]
    for fila in filas:
        celdas = [_limpiar_markdown(c).strip() for c in fila.split("|")[1:-1]]
        if len(celdas) < 2:
            continue
        m_score = _RE_DIM_SCORE.search(celdas[1] or "")
        if not m_score:
            continue
        m_num = _RE_DIM_NUM.search(celdas[0] or "")
        num = int(m_num.group(1)) if m_num else len(out["dims"]) + 1
        out["dims"].append({
            "num": num,
            "score": int(m_score.group(1)),
            "max": int(m_score.group(2)),
            "texto": fila,
            "just": celdas[2] if len(celdas) > 2 else "",
        })

    m_total = _RE_TOTAL.search(texto_limpio)
    if m_total:
        out["total"] = int(m_total.group(1))
    elif len(out["dims"]) == 5:
        out["total"] = sum(d["score"] for d in out["dims"])

    # La ÚLTIMA ocurrencia, no la primera: el informe puede citar el nombre de
    # la sección antes de escribirla de verdad.
    sin_fences = _sin_bloques_de_codigo(texto_limpio)
    encabezados = list(_RE_BANDERAS_HEADER.finditer(sin_fences))
    m_band = encabezados[-1] if encabezados else None
    if m_band:
        texto_limpio = sin_fences
        resto = texto_limpio[m_band.end():]
        m_next = _RE_NEXT_HEADER.search(resto)
        bloque = texto_limpio[m_band.start():m_band.end() + (m_next.start() if m_next else len(resto))]
        vistas = []
        for mb in _RE_BANDERA_ITEM.finditer(bloque):
            if mb.group(1) not in vistas:
                vistas.append(mb.group(1))
        out["banderas"] = vistas
        out["ningunaBandera"] = bool(_RE_NINGUNA_BANDERA.search(bloque)) and not vistas
    else:
        out["sinSeccionBanderas"] = True

    out["tieneSugerencia"] = bool(_RE_SUGERENCIA.search(texto_limpio))
    return out


def validar(texto: str, dump_count: int | None = None) -> dict:
    """`dump_count`, cuando está disponible (la corrida automática lo tiene:
    es dump["count"], la cantidad real de archivos que se le mandaron al
    modelo), permite comparar contra un número exacto en vez de un umbral fijo
    — así un repositorio que genuinamente solo tiene 1 archivo relevante (por
    ejemplo, un repo público sin ninguna estructura de trabajo final) no se
    rechaza como si el agente no hubiera leído nada."""
    p = parse_correccion(texto)
    resultados = []
    criticos = 0
    avisos = 0

    def agregar(estado, titulo, detalle=""):
        nonlocal criticos, avisos
        resultados.append({"estado": estado, "titulo": titulo, "detalle": detalle})
        if estado == "bad":
            criticos += 1
        elif estado == "warn":
            avisos += 1

    if p["archivosLeidos"] is None:
        agregar("bad", "Falta la línea de trazabilidad", 'No aparece "Archivos leídos: N".')
    elif dump_count is not None:
        if p["archivosLeidos"] != dump_count:
            agregar("bad", f"Declara haber leído {p['archivosLeidos']} archivo(s), pero se le entregaron {dump_count}",
                    "El número tiene que coincidir con lo que realmente se le mandó — si no coincide, o mintió o perdió la cuenta.")
        else:
            agregar("ok", f"Leyó los {p['archivosLeidos']} archivo(s) que se le entregaron")
    elif p["archivosLeidos"] <= 1:
        # Sin dump_count (modo manual: la corrida pasó por un chat externo, no
        # tenemos con qué comparar) no podemos distinguir "no leyó nada" de
        # "el repo genuinamente tiene 1 archivo" — queda como aviso visible,
        # no como rechazo automático.
        agregar("warn", f"Solo declara {p['archivosLeidos']} archivo(s) leído(s)",
                "Puede ser que el agente no haya leído el repositorio, o que el repositorio realmente tenga muy poco para leer. Revisalo.")
    else:
        agregar("ok", f"Leyó {p['archivosLeidos']} archivos")

    if not p["dims"]:
        agregar("bad", "No se encontró la tabla de dimensiones", "La salida no tiene el formato fijo.")
    elif len(p["dims"]) != 5:
        agregar("bad", f"Hay {len(p['dims'])} dimensiones en vez de 5")
    else:
        agregar("ok", "Las cinco dimensiones están puntuadas")

    if p["dims"]:
        malos = [d for d in p["dims"] if d["score"] not in NIVELES.get(d["max"], [])]
        if malos:
            detalle = " · ".join(f"D{d['num']}: {d['score']}/{d['max']}" for d in malos)
            agregar("bad", "Puntajes fuera de los niveles de la rúbrica", detalle)
        else:
            agregar("ok", "Todos los puntajes son niveles válidos")

        # Citar un archivo puntual tiene sentido para justificar puntaje
        # GANADO (evita que el modelo se atribuya crédito sin evidencia). Para
        # un puntaje en 0 por ausencia total ("no existe X"), exigir que cite
        # un archivo que no existe es una exigencia sin sentido — se marcó
        # como bad y así se perdían correcciones honestas de repos vacíos.
        sin_cita_con_puntaje = [d for d in p["dims"] if d["score"] > 0 and not _RE_RUTA.search(d["texto"])]
        sin_cita_en_cero = [d for d in p["dims"] if d["score"] == 0 and not _RE_RUTA.search(d["texto"])]
        if sin_cita_con_puntaje:
            agregar("bad", f"{len(sin_cita_con_puntaje)} dimensión(es) con puntaje pero sin citar archivo",
                    ", ".join(f"D{d['num']}" for d in sin_cita_con_puntaje))
        elif sin_cita_en_cero:
            agregar("warn", f"{len(sin_cita_en_cero)} dimensión(es) en 0 sin mencionar un archivo concreto",
                    ", ".join(f"D{d['num']}" for d in sin_cita_en_cero))
        else:
            agregar("ok", "Cada puntaje cita un archivo")

    if p["total"] is None:
        agregar("bad", "Falta el puntaje total")
    elif len(p["dims"]) == 5:
        suma = sum(d["score"] for d in p["dims"])
        if suma != p["total"]:
            agregar("bad", f"El total no cierra: dice {p['total']} y suma {suma}")
        else:
            agregar("ok", f"El total cierra: {suma}/100")

    if p["sinSeccionBanderas"]:
        agregar("bad", "Falta la sección de banderas de integridad")
    elif p["ningunaBandera"]:
        agregar("ok", "Revisó integridad: ninguna bandera")
    elif p["banderas"]:
        es_b4 = "B4" in p["banderas"]
        detalle = ", ".join(p["banderas"])
        if es_b4:
            detalle += " — B4: revisá que ignoró la instrucción del repo evaluado."
        agregar("warn" if es_b4 else "ok", f"Banderas reportadas: {len(p['banderas'])}", detalle)
    else:
        agregar("warn", "Sección de banderas sin conclusión clara")

    if not p["tieneSugerencia"]:
        agregar("warn", "Falta la sugerencia de mejora")
    else:
        agregar("ok", "Incluye sugerencia de mejora")

    veredicto = "bad" if criticos else ("warn" if avisos else "ok")
    return {"parsed": p, "resultados": resultados, "criticos": criticos, "avisos": avisos, "veredicto": veredicto}


def rango_de(total: int) -> dict:
    if total is None:
        return {"label": "sin total", "tipo": "muted"}
    if total >= 85:
        return {"label": "Sistema completo, honesto y reproducible", "tipo": "ok"}
    if total >= 70:
        return {"label": "Sólido con huecos identificables", "tipo": "ok"}
    if total >= 55:
        return {"label": "Funciona pero el proceso o la evidencia están flojos", "tipo": "warn"}
    if total >= 40:
        return {"label": "Entrega parcial: falta una dimensión entera", "tipo": "warn"}
    return {"label": "No cumple los requisitos mínimos", "tipo": "bad"}

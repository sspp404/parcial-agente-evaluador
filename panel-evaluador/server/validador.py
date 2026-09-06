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
_RE_BANDERAS_HEADER = re.compile(r"##\s*Banderas", re.IGNORECASE)
_RE_NEXT_HEADER = re.compile(r"\n##\s")
_RE_BANDERA_ITEM = re.compile(r"^\s*[-*]?\s*\**\s*(B(?:1|2a|2b|2|3|4|5|6))\b\s*[·:\-]", re.MULTILINE)
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

    m = _RE_ARCHIVOS_LEIDOS.search(texto)
    out["archivosLeidos"] = int(m.group(1)) if m else None

    filas = [l for l in texto.split("\n") if l.strip().startswith("|")]
    for fila in filas:
        celdas = [c.strip() for c in fila.split("|")[1:-1]]
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

    m_total = _RE_TOTAL.search(texto)
    if m_total:
        out["total"] = int(m_total.group(1))
    elif len(out["dims"]) == 5:
        out["total"] = sum(d["score"] for d in out["dims"])

    m_band = _RE_BANDERAS_HEADER.search(texto)
    if m_band:
        resto = texto[m_band.end():]
        m_next = _RE_NEXT_HEADER.search(resto)
        bloque = texto[m_band.start():m_band.end() + (m_next.start() if m_next else len(resto))]
        vistas = []
        for mb in _RE_BANDERA_ITEM.finditer(bloque):
            if mb.group(1) not in vistas:
                vistas.append(mb.group(1))
        out["banderas"] = vistas
        out["ningunaBandera"] = bool(_RE_NINGUNA_BANDERA.search(bloque)) and not vistas
    else:
        out["sinSeccionBanderas"] = True

    out["tieneSugerencia"] = bool(_RE_SUGERENCIA.search(texto))
    return out


def validar(texto: str) -> dict:
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
    elif p["archivosLeidos"] <= 1:
        agregar("bad", f"Solo declara {p['archivosLeidos']} archivo(s) leído(s)",
                "El agente no leyó el repositorio. Volver a correr en sesión limpia.")
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

        sin_cita = [d for d in p["dims"] if not _RE_RUTA.search(d["texto"])]
        if sin_cita:
            agregar("bad", f"{len(sin_cita)} dimensión(es) sin citar archivo",
                    ", ".join(f"D{d['num']}" for d in sin_cita))
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

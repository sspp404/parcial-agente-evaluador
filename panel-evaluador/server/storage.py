"""
Persistencia de proyectos y correcciones — un archivo JSON local, con lock
porque el servidor es multi-thread (ThreadingHTTPServer).

Reemplaza el localStorage del navegador de la versión anterior: antes, abrir
la app desde un archivo local (file://) hacía que cada navegador tuviera su
propio localStorage aislado, así que el estado no era ni compartible ni
confiable. Ahora vive en un solo lugar en disco.
"""
import json
import re
import threading
import time
import uuid
from pathlib import Path

_LOCK = threading.Lock()


def _uid() -> str:
    return uuid.uuid4().hex[:12]


_RE_ID = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_RE_FECHA = re.compile(r"^\d{4}-\d{2}-\d{2}$")
_RE_BANDERA = re.compile(r"^B[1-6][ab]?$")


def _texto(v, maximo: int = 400) -> str:
    return v[:maximo] if isinstance(v, str) else ""


def _saneado_proyecto(p) -> dict | None:
    if not isinstance(p, dict) or not _RE_ID.match(str(p.get("id", ""))):
        return None
    limpio = dict(p)
    limpio["id"] = str(p["id"])
    for campo in ("nombre", "ruta", "url", "origen", "creado"):
        if campo in limpio:
            limpio[campo] = _texto(limpio[campo], 500)
    return limpio


def _saneado_correccion(c) -> dict | None:
    if not isinstance(c, dict) or not _RE_ID.match(str(c.get("id", ""))):
        return None
    if not _RE_ID.match(str(c.get("projectId", ""))):
        return None
    limpio = dict(c)
    limpio["id"] = str(c["id"])
    limpio["projectId"] = str(c["projectId"])
    fecha = str(c.get("fecha", ""))
    limpio["fecha"] = fecha if _RE_FECHA.match(fecha) else ""
    total = c.get("total")
    limpio["total"] = total if isinstance(total, int) and 0 <= total <= 100 else None
    limpio["veredicto"] = c["veredicto"] if c.get("veredicto") in ("ok", "warn", "bad") else "bad"
    limpio["banderas"] = [b for b in (c.get("banderas") or []) if isinstance(b, str) and _RE_BANDERA.match(b)]
    limpio["raw"] = _texto(c.get("raw", ""), 200_000)
    return limpio


class Storage:
    def __init__(self, path: Path):
        self.path = path

    def _load(self) -> dict:
        if not self.path.exists():
            return {"projects": [], "corrections": []}
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {"projects": [], "corrections": []}

    def _save(self, state: dict) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")
        tmp.replace(self.path)

    # ---------- proyectos ----------
    def list_projects(self) -> list:
        with _LOCK:
            return self._load()["projects"]

    def create_project(self, data: dict) -> dict:
        with _LOCK:
            state = self._load()
            proj = {
                "id": _uid(),
                "nombre": data.get("nombre", "").strip(),
                "origen": data.get("origen", "url"),
                "url": data.get("url", "").strip(),
                "ruta": data.get("ruta", "").strip() or "../trabajo-a-corregir/",
                "creado": data.get("creado") or time.strftime("%Y-%m-%d"),
            }
            state["projects"].append(proj)
            self._save(state)
            return proj

    def importar_urls(self, urls: list) -> dict:
        """Crea un proyecto por cada URL de GitHub de la lista, en un solo
        golpe — pensado para pegar 50 links de una vez en vez de crear
        proyectos de a uno. Ignora líneas vacías, evita duplicar un
        proyecto que ya apunta a la misma URL (podés volver a pegar la
        misma lista con dos links nuevos y no te duplica los 48 viejos)."""
        creados, duplicados, invalidos = [], [], []
        with _LOCK:
            state = self._load()
            urls_existentes = {p["url"] for p in state["projects"] if p.get("url")}
            for linea in urls:
                url = linea.strip()
                if not url:
                    continue
                m = re.match(r"^https?://github\.com/([^/\s]+)/([^/\s]+?)(?:\.git)?/?$", url)
                if not m:
                    invalidos.append(url)
                    continue
                if url in urls_existentes:
                    duplicados.append(url)
                    continue
                owner, repo = m.group(1), m.group(2)
                nombre = f"{owner}/{repo}"
                ruta = f"../repos-a-corregir/{owner}-{repo}"
                proj = {
                    "id": _uid(),
                    "nombre": nombre,
                    "origen": "url",
                    "url": url,
                    "ruta": ruta,
                    "creado": time.strftime("%Y-%m-%d"),
                }
                state["projects"].append(proj)
                urls_existentes.add(url)
                creados.append(proj)
            self._save(state)
        return {"creados": creados, "duplicados": duplicados, "invalidos": invalidos}

    def update_project(self, project_id: str, data: dict) -> dict | None:
        with _LOCK:
            state = self._load()
            for p in state["projects"]:
                if p["id"] == project_id:
                    for k in ("nombre", "origen", "url", "ruta"):
                        if k in data:
                            p[k] = data[k]
                    self._save(state)
                    return p
            return None

    def delete_project(self, project_id: str) -> int:
        with _LOCK:
            state = self._load()
            before = len(state["corrections"])
            state["projects"] = [p for p in state["projects"] if p["id"] != project_id]
            state["corrections"] = [c for c in state["corrections"] if c["projectId"] != project_id]
            borradas = before - len(state["corrections"])
            self._save(state)
            return borradas

    # ---------- correcciones ----------
    def list_corrections(self) -> list:
        with _LOCK:
            return self._load()["corrections"]

    def create_correction(self, data: dict) -> dict:
        with _LOCK:
            state = self._load()
            corr = {
                "id": _uid(),
                "projectId": data["projectId"],
                "fecha": data.get("fecha"),
                "raw": data["raw"],
                "total": data.get("total"),
                "dims": data.get("dims", []),
                "banderas": data.get("banderas", []),
                "archivosLeidos": data.get("archivosLeidos"),
                "veredicto": data.get("veredicto"),
                "guardado": time.strftime("%Y-%m-%dT%H:%M:%S"),
            }
            state["corrections"].append(corr)
            self._save(state)
            return corr

    def delete_correction(self, correction_id: str) -> bool:
        with _LOCK:
            state = self._load()
            before = len(state["corrections"])
            state["corrections"] = [c for c in state["corrections"] if c["id"] != correction_id]
            self._save(state)
            return len(state["corrections"]) < before

    # ---------- export / import ----------
    def export_all(self) -> dict:
        with _LOCK:
            state = self._load()
            return {"projects": state["projects"], "corrections": state["corrections"]}

    def import_all(self, data: dict, modo: str = "merge") -> dict:
        # Un backup es un .json que el usuario elige de su disco: puede venir de
        # otra máquina, de un compañero o de cualquier lado. Antes se guardaba tal
        # cual y el frontend después interpolaba `id`, `fecha`, `total`, `veredicto`
        # y `banderas` en el HTML — un backup preparado a mano inyectaba markup y
        # handlers. Se sanea acá, en la entrada, y no en los seis lugares donde se
        # renderiza: si el dato entra limpio, no hay que acordarse de escaparlo.
        data = {
            "projects": [x for x in (_saneado_proyecto(p) for p in data.get("projects", []) or []) if x],
            "corrections": [x for x in (_saneado_correccion(c) for c in data.get("corrections", []) or []) if x],
        }
        with _LOCK:
            state = self._load()
            if modo == "replace":
                state = {"projects": data.get("projects", []), "corrections": data.get("corrections", [])}
            else:
                ids_p = {p["id"] for p in state["projects"]}
                for p in data.get("projects", []):
                    if p["id"] not in ids_p:
                        state["projects"].append(p)
                ids_c = {c["id"] for c in state["corrections"]}
                for c in data.get("corrections", []):
                    if c["id"] not in ids_c:
                        state["corrections"].append(c)
            self._save(state)
            return {"projects": len(state["projects"]), "corrections": len(state["corrections"])}

"""
Persistencia de proyectos y correcciones — un archivo JSON local, con lock
porque el servidor es multi-thread (ThreadingHTTPServer).

Reemplaza el localStorage del navegador de la versión anterior: antes, abrir
la app desde un archivo local (file://) hacía que cada navegador tuviera su
propio localStorage aislado, así que el estado no era ni compartible ni
confiable. Ahora vive en un solo lugar en disco.
"""
import json
import threading
import time
import uuid
from pathlib import Path

_LOCK = threading.Lock()


def _uid() -> str:
    return uuid.uuid4().hex[:12]


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

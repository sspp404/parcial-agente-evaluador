#!/usr/bin/env python3
"""
Backend del Panel del agente evaluador. Corre 100% local: escucha solo en
127.0.0.1, nunca en la red. Sirve el frontend (web/) y una API JSON (/api/*).

Arranque:
    python server/app.py
o simplemente hacé doble click en iniciar.bat (Windows).

La API key de Anthropic no vive acá: la trae Doppler en el momento en que
hace falta (ver doppler_client.py). Lo único que este proceso guarda en
disco es la contraseña de acceso al panel (hasheada) y los proyectos /
correcciones que vas cargando.
"""
import json
import mimetypes
import os
import re
import subprocess
import sys
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from http.cookies import SimpleCookie
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Consola de Windows en cp1252 rompe con acentos/flechas si no forzamos utf-8.
try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except AttributeError:
    pass

SERVER_DIR = Path(__file__).resolve().parent
BASE_DIR = SERVER_DIR.parent                 # panel-evaluador/
CORRECTOR_DIR = BASE_DIR.parent              # parcial-agente-evaluador/ (auto-detectado)
DATA_DIR = BASE_DIR / "data"
WEB_DIR = BASE_DIR / "web"
DATA_DIR.mkdir(exist_ok=True)

sys.path.insert(0, str(SERVER_DIR))
import auth as auth_mod
import doppler_client
import corrector
import storage as storage_mod
import validador
import anthropic_client

AUTH = auth_mod.Auth(DATA_DIR)
STORAGE = storage_mod.Storage(DATA_DIR / "state.json")
PORT = int(os.environ.get("PORT", "8765"))
COOKIE_NAME = "panel_session"

CONTENT_TYPES = {".html": "text/html; charset=utf-8", ".css": "text/css; charset=utf-8",
                  ".js": "application/javascript; charset=utf-8", ".svg": "image/svg+xml"}


def json_bytes(obj) -> bytes:
    return json.dumps(obj, ensure_ascii=False).encode("utf-8")


class Handler(BaseHTTPRequestHandler):
    server_version = "PanelEvaluador/1.0"

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

    # ---------- helpers de request/response ----------
    def _session_token(self) -> str | None:
        raw = self.headers.get("Cookie")
        if not raw:
            return None
        cookie = SimpleCookie()
        cookie.load(raw)
        morsel = cookie.get(COOKIE_NAME)
        return morsel.value if morsel else None

    def _require_session(self) -> bool:
        if AUTH.check_session(self._session_token()):
            return True
        self._send_json({"error": "No autenticado."}, status=401)
        return False

    def _read_json_body(self) -> dict:
        length = int(self.headers.get("Content-Length", 0) or 0)
        if length == 0:
            return {}
        raw = self.rfile.read(length)
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            return {}

    def _send_json(self, obj, status=200, set_cookie: str | None = None):
        body = json_bytes(obj)
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        if set_cookie is not None:
            if set_cookie == "":
                self.send_header("Set-Cookie", f"{COOKIE_NAME}=; Path=/; HttpOnly; Max-Age=0")
            else:
                self.send_header("Set-Cookie", f"{COOKIE_NAME}={set_cookie}; Path=/; HttpOnly; SameSite=Lax")
        self.end_headers()
        self.wfile.write(body)

    def _send_file(self, path: Path):
        if not path.exists() or not path.is_file():
            self._send_json({"error": "No encontrado."}, status=404)
            return
        ctype = CONTENT_TYPES.get(path.suffix.lower()) or mimetypes.guess_type(str(path))[0] or "application/octet-stream"
        data = path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(data)))
        # Esta app se edita en caliente durante el desarrollo: sin esto, el
        # navegador puede quedarse sirviendo una versión vieja de app.js/
        # styles.css desde su caché aunque el archivo en disco ya cambió, y
        # parece un bug fantasma que "a veces sí, a veces no" se corrige solo.
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    # ---------- ruteo ----------
    def do_GET(self):
        parsed = urlparse(self.path)
        route = parsed.path
        qs = parse_qs(parsed.query)

        if route.startswith("/api/"):
            return self._api_get(route, qs)

        # estático: / -> index.html, resto se resuelve dentro de web/
        rel = route.lstrip("/") or "index.html"
        candidate = (WEB_DIR / rel).resolve()
        if WEB_DIR not in candidate.parents and candidate != WEB_DIR:
            self._send_json({"error": "Ruta inválida."}, status=400)
            return
        if not candidate.exists():
            candidate = WEB_DIR / "index.html"
        self._send_file(candidate)

    def do_POST(self):
        parsed = urlparse(self.path)
        self._api_post(parsed.path)

    def do_DELETE(self):
        parsed = urlparse(self.path)
        self._api_delete(parsed.path)

    def do_PUT(self):
        parsed = urlparse(self.path)
        self._api_put(parsed.path)

    def do_HEAD(self):
        # Algunos navegadores/herramientas prueban con HEAD antes del GET real.
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()

    # ---------- API: GET ----------
    def _api_get(self, route, qs):
        if route == "/api/auth/status":
            self._send_json({
                "needsSetup": not AUTH.is_initialized(),
                "loggedIn": AUTH.check_session(self._session_token()),
            })
            return

        if not self._require_session():
            return

        if route == "/api/projects":
            self._send_json({"projects": STORAGE.list_projects()})
            return

        if route == "/api/corrections":
            self._send_json({"corrections": STORAGE.list_corrections()})
            return

        if route == "/api/doppler/status":
            self._send_json(doppler_client.status(DATA_DIR))
            return

        if route == "/api/fs/verificar":
            ruta = (qs.get("ruta") or [""])[0]
            self._send_json(corrector.verificar_carpeta(ruta, CORRECTOR_DIR))
            return

        if route == "/api/fs/browse":
            ruta = (qs.get("ruta") or [None])[0]
            self._send_json(corrector.listar_subcarpetas(ruta, CORRECTOR_DIR))
            return

        if route == "/api/fs/corrector-status":
            cf = corrector.cargar_archivos_corrector(CORRECTOR_DIR)
            self._send_json({
                "encontrado": cf is not None,
                "ruta": str(CORRECTOR_DIR),
            })
            return

        if route == "/api/fs/rubrica":
            cf = corrector.cargar_archivos_corrector(CORRECTOR_DIR)
            if not cf:
                self._send_json({"error": f"No se encontró rubrica.md o agente/system_prompt.md en {CORRECTOR_DIR}"}, status=404)
                return
            self._send_json({"rubrica": cf["rubrica"], "systemPrompt": cf["systemPrompt"]})
            return

        if route == "/api/export":
            self._send_json(STORAGE.export_all())
            return

        self._send_json({"error": "No encontrado."}, status=404)

    # ---------- API: POST ----------
    def _api_post(self, route):
        if route == "/api/auth/setup":
            body = self._read_json_body()
            pw1, pw2 = body.get("password", ""), body.get("password2", "")
            if len(pw1) < 4:
                self._send_json({"error": "Usá al menos 4 caracteres."}, status=400)
                return
            if pw1 != pw2:
                self._send_json({"error": "Las dos contraseñas no coinciden."}, status=400)
                return
            if AUTH.is_initialized():
                self._send_json({"error": "Ya existe una contraseña configurada."}, status=400)
                return
            token = AUTH.setup(pw1)
            self._send_json({"ok": True}, set_cookie=token)
            return

        if route == "/api/auth/login":
            body = self._read_json_body()
            token, error = AUTH.login(body.get("password", ""), ip=self.client_address[0])
            if error:
                self._send_json({"error": error}, status=401)
                return
            self._send_json({"ok": True}, set_cookie=token)
            return

        if route == "/api/auth/logout":
            AUTH.logout(self._session_token())
            self._send_json({"ok": True}, set_cookie="")
            return

        if route == "/api/auth/reset":
            body = self._read_json_body()
            if body.get("confirm") is not True:
                self._send_json({"error": "Falta confirmar."}, status=400)
                return
            AUTH.wipe()
            (DATA_DIR / "state.json").unlink(missing_ok=True)
            doppler_client.clear_token_file(DATA_DIR)
            self._send_json({"ok": True}, set_cookie="")
            return

        # ---- todo lo demás requiere sesión ----
        if not self._require_session():
            return

        if route == "/api/projects":
            body = self._read_json_body()
            if not body.get("nombre", "").strip():
                self._send_json({"error": "Ponele un nombre al proyecto."}, status=400)
                return
            self._send_json({"project": STORAGE.create_project(body)})
            return

        if route == "/api/corrections":
            body = self._read_json_body()
            if not body.get("projectId"):
                self._send_json({"error": "Falta el proyecto."}, status=400)
                return
            raw = body.get("raw", "")
            v = validador.validar(raw)
            if v["veredicto"] == "bad":
                self._send_json({"error": "La corrección no pasa la validación mínima.", "validacion": v}, status=422)
                return
            corr = STORAGE.create_correction({
                "projectId": body["projectId"],
                "fecha": body.get("fecha"),
                "raw": raw,
                "total": v["parsed"]["total"],
                "dims": [{"num": d["num"], "score": d["score"], "max": d["max"]} for d in v["parsed"]["dims"]],
                "banderas": v["parsed"]["banderas"],
                "archivosLeidos": v["parsed"]["archivosLeidos"],
                "veredicto": v["veredicto"],
            })
            self._send_json({"correction": corr, "validacion": v})
            return

        if route == "/api/validar":
            body = self._read_json_body()
            v = validador.validar(body.get("texto", ""))
            self._send_json({"validacion": v})
            return

        if route == "/api/doppler/token":
            body = self._read_json_body()
            token = body.get("token", "").strip()
            if not token:
                self._send_json({"error": "Pegá un token."}, status=400)
                return
            try:
                doppler_client.validate_token(token)   # nunca se persiste un token que falla
            except doppler_client.DopplerError as e:
                self._send_json({"error": str(e)}, status=400)
                return
            doppler_client.set_token_file(DATA_DIR, token)
            self._send_json(doppler_client.status(DATA_DIR))
            return

        if route == "/api/doppler/test":
            st = doppler_client.status(DATA_DIR)
            self._send_json(st)
            return

        if route == "/api/fs/clone":
            body = self._read_json_body()
            self._clonar_repo(body.get("url", ""), body.get("ruta", ""))
            return

        if route == "/api/run/auto":
            self._correr_automatico(self._read_json_body())
            return

        if route == "/api/import":
            body = self._read_json_body()
            resultado = STORAGE.import_all(body.get("data", {}), modo=body.get("modo", "merge"))
            self._send_json(resultado)
            return

        self._send_json({"error": "No encontrado."}, status=404)

    # ---------- API: PUT / DELETE ----------
    def _api_put(self, route):
        if not self._require_session():
            return
        parts = route.split("/")
        if len(parts) == 4 and parts[1] == "api" and parts[2] == "projects":
            body = self._read_json_body()
            proj = STORAGE.update_project(parts[3], body)
            if proj is None:
                self._send_json({"error": "Proyecto no encontrado."}, status=404)
                return
            self._send_json({"project": proj})
            return
        self._send_json({"error": "No encontrado."}, status=404)

    def _api_delete(self, route):
        if not self._require_session():
            return
        parts = route.split("/")
        if len(parts) == 4 and parts[1] == "api" and parts[2] == "projects":
            borradas = STORAGE.delete_project(parts[3])
            self._send_json({"ok": True, "correccionesBorradas": borradas})
            return
        if len(parts) == 4 and parts[1] == "api" and parts[2] == "corrections":
            ok = STORAGE.delete_correction(parts[3])
            self._send_json({"ok": ok})
            return
        self._send_json({"error": "No encontrado."}, status=404)

    # ---------- operaciones más largas ----------
    def _clonar_repo(self, url: str, ruta: str):
        if not url:
            self._send_json({"error": "Falta la URL del repositorio."}, status=400)
            return
        # url viene de un campo que en la práctica se llena con el link de OTRO
        # grupo (dato de terceros) — no hay que confiar en que tenga forma de URL.
        # Sin este chequeo, una cadena que empiece con "-" puede interpretarse
        # como una opción de git en vez de un repositorio (inyección de
        # argumentos: por ejemplo --upload-pack= puede ejecutar un comando).
        if not re.match(r"^(https?://|git@|ssh://)", url):
            self._send_json({"error": "La URL tiene que empezar con https://, git@ o ssh:// — no se acepta otro formato."}, status=400)
            return
        destino = Path(ruta or "../trabajo-a-corregir/").expanduser()
        if not destino.is_absolute():
            destino = (CORRECTOR_DIR / destino).resolve()
        if destino.exists() and any(destino.iterdir()):
            self._send_json({"error": f"La carpeta destino ya existe y no está vacía: {destino}"}, status=400)
            return
        destino.parent.mkdir(parents=True, exist_ok=True)
        try:
            proc = subprocess.run(
                # "--" le dice a git que lo que sigue son argumentos posicionales,
                # nunca opciones, aunque url o destino empezaran con "-".
                ["git", "clone", "--depth", "1", "--", url, str(destino)],
                capture_output=True, text=True, timeout=120,
            )
        except FileNotFoundError:
            self._send_json({"error": "No se encontró 'git' en el sistema. Cloná el repo a mano y usá el modo manual."}, status=500)
            return
        except subprocess.TimeoutExpired:
            self._send_json({"error": "git clone tardó demasiado (timeout de 120s)."}, status=504)
            return
        if proc.returncode != 0:
            self._send_json({"error": f"git clone falló: {proc.stderr.strip()[-400:]}"}, status=400)
            return
        info = corrector.verificar_carpeta(str(destino), CORRECTOR_DIR)
        self._send_json({"ok": True, "ruta": str(destino), "info": info})

    def _correr_automatico(self, body: dict):
        project_id = body.get("projectId")
        fecha = body.get("fecha") or time.strftime("%Y-%m-%d")
        proyectos = {p["id"]: p for p in STORAGE.list_projects()}
        proyecto = proyectos.get(project_id)
        if not proyecto:
            self._send_json({"error": "Proyecto no encontrado."}, status=404)
            return

        cf = corrector.cargar_archivos_corrector(CORRECTOR_DIR)
        if not cf:
            self._send_json({"error": f"No se encontró rubrica.md o agente/system_prompt.md en {CORRECTOR_DIR}"}, status=500)
            return

        try:
            dump = corrector.construir_dump(proyecto["ruta"], CORRECTOR_DIR)
        except corrector.RutaInvalida as e:
            self._send_json({"error": str(e)}, status=400)
            return
        if dump["count"] == 0:
            self._send_json({"error": f"La carpeta {proyecto['ruta']} no tiene archivos legibles (¿ruta correcta?)."}, status=400)
            return

        try:
            creds = doppler_client.get_credentials(DATA_DIR)
        except doppler_client.DopplerError as e:
            self._send_json({"error": str(e)}, status=400)
            return

        # Bloque fijo (cacheable) + bloque variable — misma lógica que usa
        # calibrar.py, factorizada en corrector.construir_prompts().
        cached_prefix, user_text = corrector.construir_prompts(proyecto["nombre"], fecha, cf["rubrica"], dump)

        try:
            resultado_llamada = anthropic_client.call(
                creds["apiKey"], creds["model"], cf["systemPrompt"], user_text, cached_prefix=cached_prefix
            )
        except anthropic_client.AnthropicError as e:
            self._send_json({"error": str(e)}, status=502)
            return

        salida = resultado_llamada["text"]
        v = validador.validar(salida)
        self._send_json({
            "salida": salida,
            "validacion": v,
            "truncado": resultado_llamada["truncado"],
            "usage": resultado_llamada["usage"],
            "dump": {
                "count": dump["count"], "totalChars": dump["totalChars"], "cortado": dump["cortado"],
                "omitidos": dump["omitidos"], "totalArchivos": dump["totalArchivos"],
                "alertasSeguridad": dump["alertasSeguridad"], "gitLog": dump["gitLog"],
            },
            "modelo": creds["model"],
        })


def main():
    if not WEB_DIR.exists():
        print(f"No se encontró la carpeta web/ en {WEB_DIR}", file=sys.stderr)
        sys.exit(1)
    server = ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
    url = f"http://127.0.0.1:{PORT}"
    print(f"Panel del agente evaluador corriendo en {url}")
    print(f"Corrector detectado en: {CORRECTOR_DIR}")
    print("Solo escucha en 127.0.0.1 (no accesible desde la red). Ctrl+C para cortar.")
    try:
        webbrowser.open(url)
    except Exception:
        pass
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nCerrando servidor…")
        server.shutdown()


if __name__ == "__main__":
    main()

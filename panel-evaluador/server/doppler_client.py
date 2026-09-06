"""
Resuelve de dónde sale la ANTHROPIC_API_KEY para correr una corrección, con
dos caminos posibles:

1. **Doppler** (el nuestro, el recomendado para el grupo) — la key nunca
   vive en ningún archivo de este repo ni de esta app: vive en Doppler, y
   acá solo se la pide prestada. Requiere un Service Token de Doppler (de
   solo lectura), que sí tiene que vivir en algún lado de esta máquina para
   poder pedirle credenciales a Doppler — ese es el único secreto "local"
   que queda, y es uno acotado y revocable desde el dashboard de Doppler en
   cualquier momento, a diferencia de la API key real de Anthropic.

   Cómo se resuelve el token de Doppler, en orden:
   a. Variable de entorno DOPPLER_TOKEN (recomendado: `setx DOPPLER_TOKEN
      "..."` en Windows — nunca toca ningún archivo de la app).
   b. data/doppler_token.txt, si se cargó una vez desde la pantalla de
      Configuración. Vive dentro de panel-evaluador/, que ya
      está fuera de git por el .gitignore de la raíz del repo del parcial.

2. **Variable de entorno `ANTHROPIC_API_KEY` directa** — el atajo para
   cualquiera que no es nosotros: un profesor o compañero que clona este
   repo y quiere probar la app con su propia cuenta de Anthropic, sin tener
   que crearse una cuenta de Doppler solo para eso. Se usa únicamente si no
   hay ningún token de Doppler configurado — Doppler tiene prioridad para
   nuestro propio uso.
"""
import json
import os
import time
import urllib.error
import urllib.request
from pathlib import Path

DOWNLOAD_URL = "https://api.doppler.com/v3/configs/config/secrets/download?format=json"
CACHE_TTL_SECONDS = 300  # 5 minutos — evita pegarle a Doppler en cada click


class DopplerError(RuntimeError):
    """Mensaje ya pensado para mostrarse tal cual en la UI."""


_cache = {"at": 0.0, "secrets": None}


def _token_file(data_dir: Path) -> Path:
    return data_dir / "doppler_token.txt"


def get_token(data_dir: Path) -> str | None:
    env = os.environ.get("DOPPLER_TOKEN", "").strip()
    if env:
        return env
    f = _token_file(data_dir)
    if f.exists():
        value = f.read_text(encoding="utf-8").strip()
        return value or None
    return None


def token_source(data_dir: Path) -> str | None:
    """Para mostrar en la UI de dónde vino el token, sin mostrar el token."""
    if os.environ.get("DOPPLER_TOKEN", "").strip():
        return "variable de entorno DOPPLER_TOKEN"
    if _token_file(data_dir).exists():
        return "archivo local (data/doppler_token.txt)"
    return None


def set_token_file(data_dir: Path, token: str) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    _token_file(data_dir).write_text(token.strip(), encoding="utf-8")
    _cache["at"] = 0.0  # invalida el cache: la próxima lectura usa el token nuevo


def clear_token_file(data_dir: Path) -> None:
    _token_file(data_dir).unlink(missing_ok=True)
    _cache["at"] = 0.0


def _download(token: str) -> dict:
    req = urllib.request.Request(
        DOWNLOAD_URL,
        headers={"Authorization": f"Bearer {token}", "accept": "application/json"},
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode("utf-8")
        except Exception:
            pass
        if e.code == 401:
            raise DopplerError("Doppler rechazó el token (401 no autorizado). Revisá que esté bien copiado y no haya sido revocado.")
        if e.code == 403:
            raise DopplerError("El token no tiene permiso de lectura sobre este config (403).")
        raise DopplerError(f"Doppler devolvió un error HTTP {e.code}: {body[:200]}")
    except urllib.error.URLError as e:
        raise DopplerError(f"No se pudo conectar a Doppler: {e.reason}")
    except (TimeoutError, OSError) as e:
        raise DopplerError(f"Doppler no respondió a tiempo: {e}")


def validate_token(token: str) -> dict:
    """Prueba un token SIN guardarlo. Usado antes de persistirlo, para no
    dejar en disco un token que ni siquiera funciona."""
    return _download(token)  # lanza DopplerError si es inválido


def fetch_secrets(data_dir: Path, force: bool = False) -> dict:
    token = get_token(data_dir)
    if not token:
        raise DopplerError(
            "No hay ningún DOPPLER_TOKEN configurado. Generá un Service Token de "
            "solo lectura en dashboard.doppler.com → tu proyecto → Service Tokens, "
            "y cargalo en Configuración o como variable de entorno."
        )
    now = time.time()
    if not force and _cache["secrets"] is not None and (now - _cache["at"]) < CACHE_TTL_SECONDS:
        return _cache["secrets"]
    secrets_dict = _download(token)
    _cache["secrets"] = secrets_dict
    _cache["at"] = now
    return secrets_dict


def _credenciales_env_directo() -> dict | None:
    """El atajo para cualquiera que no tenga Doppler configurado: una
    ANTHROPIC_API_KEY puesta directo como variable de entorno."""
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        return None
    model = os.environ.get("ANTHROPIC_MODEL", "").strip() or "claude-sonnet-5"
    return {"apiKey": api_key, "model": model, "fuente": "env_directo"}


def get_credentials(data_dir: Path, force: bool = False) -> dict:
    """{"apiKey": ..., "model": ..., "fuente": "doppler"|"env_directo"}.
    Prioridad: Doppler primero (si hay token configurado); si no hay ningún
    token de Doppler, cae a ANTHROPIC_API_KEY directa. Si hay token de
    Doppler pero está roto (401, sin el secreto cargado, etc.), se informa
    ESE error puntual en vez de caer en silencio al atajo — así un token de
    Doppler vencido no se disfraza de "no configuraste nada"."""
    if get_token(data_dir):
        secrets_dict = fetch_secrets(data_dir, force=force)
        api_key = secrets_dict.get("ANTHROPIC_API_KEY")
        if not api_key:
            raise DopplerError(
                "Se pudo conectar a Doppler, pero el config no tiene cargado un secreto "
                "llamado ANTHROPIC_API_KEY."
            )
        model = secrets_dict.get("ANTHROPIC_MODEL") or "claude-sonnet-5"
        return {"apiKey": api_key, "model": model, "fuente": "doppler"}

    directo = _credenciales_env_directo()
    if directo:
        return directo

    raise DopplerError(
        "No hay ninguna fuente de API key configurada. Para el grupo: generá un Service "
        "Token de solo lectura en dashboard.doppler.com y definilo como DOPPLER_TOKEN. "
        "Para probar la app suelta con tu propia cuenta: definí ANTHROPIC_API_KEY como "
        "variable de entorno con tu clave de Anthropic — no hace falta Doppler para eso."
    )


def status(data_dir: Path) -> dict:
    """Para la pantalla de Configuración. Nunca devuelve la key completa."""
    tiene_token_doppler = bool(get_token(data_dir))
    if not tiene_token_doppler and not _credenciales_env_directo():
        return {"connected": False, "hasToken": False, "error": None}
    try:
        creds = get_credentials(data_dir)
    except DopplerError as e:
        return {"connected": False, "hasToken": tiene_token_doppler, "error": str(e)}

    k = creds["apiKey"]
    masked = (k[:7] + "…" + k[-4:]) if len(k) > 14 else "•" * len(k)
    base = {
        "connected": True,
        "hasToken": tiene_token_doppler,
        "maskedKey": masked,
        "model": creds["model"],
        "fuente": creds["fuente"],
    }
    if creds["fuente"] == "doppler":
        secrets_dict = _cache["secrets"] or {}
        project = secrets_dict.get("DOPPLER_PROJECT")
        config = secrets_dict.get("DOPPLER_CONFIG")
        base["projectConfig"] = f"{project} / {config}" if project and config else None
        base["tokenSource"] = token_source(data_dir)
        base["cachedAt"] = _cache["at"]
    else:
        base["projectConfig"] = None
        base["tokenSource"] = "variable de entorno ANTHROPIC_API_KEY (sin Doppler)"
        base["cachedAt"] = None
    return base

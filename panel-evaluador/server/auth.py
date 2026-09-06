"""
Login del panel (candado de acceso, no un sistema de usuarios) + sesiones en
memoria del proceso.

La API key de Anthropic YA NO vive acá: la sirve Doppler (ver doppler_client.py).
Esto solo protege la puerta de entrada al panel con una contraseña que elige
quien lo instala en su máquina.
"""
import hashlib
import hmac
import json
import secrets
import time
from pathlib import Path

SCRYPT_N = 2 ** 14
SCRYPT_R = 8
SCRYPT_P = 1
KEY_LEN = 32

SESSION_TTL_SECONDS = 8 * 3600

# Freno simple a fuerza bruta: no bloquea, pero espacia intentos fallidos.
_MAX_INTENTOS_LIBRES = 5
_BLOQUEO_SEGUNDOS = 30


def _scrypt(password: str, salt: bytes) -> bytes:
    return hashlib.scrypt(
        password.encode("utf-8"), salt=salt, n=SCRYPT_N, r=SCRYPT_R, p=SCRYPT_P, dklen=KEY_LEN
    )


class Auth:
    def __init__(self, data_dir: Path):
        self.auth_file = data_dir / "auth.json"
        self._sessions: dict[str, float] = {}          # token -> expira_en
        self._intentos_fallidos: dict[str, list[float]] = {}  # ip -> [timestamps]

    # ---------- estado ----------
    def is_initialized(self) -> bool:
        return self.auth_file.exists()

    # ---------- setup / login ----------
    def setup(self, password: str) -> str:
        if self.is_initialized():
            raise RuntimeError("Ya existe una contraseña configurada.")
        salt = secrets.token_bytes(16)
        pw_hash = _scrypt(password, salt)
        self.auth_file.write_text(
            json.dumps({"salt": salt.hex(), "hash": pw_hash.hex()}), encoding="utf-8"
        )
        return self._new_session()

    def _bloqueado(self, ip: str) -> float:
        """Devuelve segundos restantes de bloqueo (0 si no está bloqueada esa IP)."""
        ahora = time.time()
        intentos = [t for t in self._intentos_fallidos.get(ip, []) if ahora - t < 300]
        self._intentos_fallidos[ip] = intentos
        if len(intentos) < _MAX_INTENTOS_LIBRES:
            return 0
        ultimo = intentos[-1]
        restante = _BLOQUEO_SEGUNDOS - (ahora - ultimo)
        return max(0.0, restante)

    def login(self, password: str, ip: str = "local") -> tuple[str | None, str | None]:
        """Devuelve (token, None) si es correcta, o (None, mensaje_error)."""
        restante = self._bloqueado(ip)
        if restante > 0:
            return None, f"Demasiados intentos fallidos. Esperá {int(restante) + 1} segundos."
        if not self.is_initialized():
            return None, "Todavía no se configuró una contraseña."
        auth = json.loads(self.auth_file.read_text(encoding="utf-8"))
        salt = bytes.fromhex(auth["salt"])
        expected = bytes.fromhex(auth["hash"])
        candidate = _scrypt(password, salt)
        if not hmac.compare_digest(candidate, expected):
            self._intentos_fallidos.setdefault(ip, []).append(time.time())
            return None, "Contraseña incorrecta."
        self._intentos_fallidos.pop(ip, None)
        return self._new_session(), None

    def _new_session(self) -> str:
        token = secrets.token_urlsafe(32)
        self._sessions[token] = time.time() + SESSION_TTL_SECONDS
        return token

    def check_session(self, token: str | None) -> bool:
        if not token:
            return False
        expira = self._sessions.get(token)
        if expira is None:
            return False
        if expira < time.time():
            self._sessions.pop(token, None)
            return False
        self._sessions[token] = time.time() + SESSION_TTL_SECONDS
        return True

    def logout(self, token: str | None) -> None:
        if token:
            self._sessions.pop(token, None)

    def wipe(self) -> None:
        self.auth_file.unlink(missing_ok=True)
        self._sessions.clear()
        self._intentos_fallidos.clear()

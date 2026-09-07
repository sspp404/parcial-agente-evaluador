"""
Llamada a la API de mensajes de Anthropic. Corre siempre del lado del
servidor: la API key (traída de Doppler en el momento) nunca cruza al
navegador.

Usa prompt caching (`cache_control`) en el system prompt y en el bloque fijo
del mensaje (la rúbrica): esos textos son idénticos en cada corrida, así que
cachearlos hace que solo la primera llamada los pague completos — las
siguientes pagan una fracción de ese bloque. En una noche con muchas
corridas seguidas (calibración, prueba de fuego), esto es la diferencia más
grande en costo, más que cualquier recorte de contenido del repo evaluado.
"""
import json
import ssl
import time
import urllib.error
import urllib.request

MESSAGES_URL = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"


class AnthropicError(RuntimeError):
    pass


def _contexto_ssl():
    """Un Python bajado de python.org en macOS viene SIN certificados raíz: el
    directorio que busca está vacío y toda conexión HTTPS muere con
    CERTIFICATE_VERIFY_FAILED. El instalador trae un "Install Certificates.command"
    para eso, pero mucha gente no lo corre nunca y el error no dice qué hacer.

    Si el paquete `certifi` está disponible, lo usamos; si no, se devuelve None y
    urllib usa la configuración por defecto (que en Linux y en el Python de
    Homebrew funciona sin más)."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return None


def call(
    api_key: str,
    model: str,
    system_text: str,
    user_text: str,
    cached_prefix: str | None = None,
    # 16000 se quedó corto en la primera corrida real contra la API: el caso
    # `oculto` lo agotó exacto y devolvió una corrección truncada a mitad de una
    # dimensión, que el validador marcó como formato inválido. La mediana real de
    # las 18 corridas fue 9.033 tokens y el máximo legítimo rondó los 14.200, así
    # que 24000 deja margen sin pagar de más: solo se cobra lo que se genera.
    max_tokens: int = 24000,
    temperature: float | None = None,
    timeout: int = 180,
) -> dict:
    """Devuelve {"text", "stop_reason", "truncado", "usage"}. El llamador
    decide qué hacer si truncado=True — no lo tira como excepción porque el
    texto parcial igual puede ser útil para diagnosticar.

    Si se pasa `cached_prefix` (por ejemplo, la rúbrica), se manda como un
    bloque de mensaje separado con cache_control — así se cachea indepen-
    dientemente del resto del contenido, que cambia en cada corrida."""
    system_blocks = [{"type": "text", "text": system_text, "cache_control": {"type": "ephemeral"}}]

    if cached_prefix:
        content = [
            {"type": "text", "text": cached_prefix, "cache_control": {"type": "ephemeral"}},
            {"type": "text", "text": user_text},
        ]
    else:
        content = user_text

    body_dict = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system_blocks,
        "messages": [{"role": "user", "content": content}],
    }
    # Los modelos de la familia "5" de Claude devuelven un HTTP 400
    # ("temperature is deprecated for this model") si se manda este parámetro
    # — a diferencia de generaciones anteriores. Por eso es opcional y nunca
    # se manda salvo que se pida explícitamente.
    if temperature is not None:
        body_dict["temperature"] = temperature
    body = json.dumps(body_dict).encode("utf-8")
    req = urllib.request.Request(
        MESSAGES_URL,
        data=body,
        method="POST",
        headers={
            "content-type": "application/json",
            "x-api-key": api_key,
            "anthropic-version": ANTHROPIC_VERSION,
        },
    )
    contexto_ssl = _contexto_ssl()
    # Un 429 (rate limit) o un 529 (sobrecarga) son transitorios: sin reintento,
    # una corrida se pierde entera por un pico de tráfico ajeno. En la prueba de
    # fuego, con varias correcciones seguidas, eso es cuestión de tiempo.
    ESPERAS = (2, 6, 15)
    ultimo_error = None
    for intento in range(len(ESPERAS) + 1):
        try:
            with urllib.request.urlopen(req, timeout=timeout, context=contexto_ssl) as resp:
                data = json.loads(resp.read().decode("utf-8"))
            break
        except urllib.error.HTTPError as e:
            msg = f"HTTP {e.code}"
            try:
                j = json.loads(e.read().decode("utf-8"))
                if j.get("error", {}).get("message"):
                    msg += " — " + j["error"]["message"]
            except Exception:
                pass
            if e.code in (429, 500, 502, 503, 529) and intento < len(ESPERAS):
                ultimo_error = msg
                time.sleep(ESPERAS[intento])
                continue
            raise AnthropicError(msg)
        except urllib.error.URLError as e:
            if intento < len(ESPERAS):
                ultimo_error = f"No se pudo conectar con Anthropic: {e.reason}"
                time.sleep(ESPERAS[intento])
                continue
            if "CERTIFICATE_VERIFY_FAILED" in str(e.reason):
                raise AnthropicError(
                    "Tu instalación de Python no tiene certificados raíz, así que no puede "
                    "validar la conexión con Anthropic. Se arregla con: "
                    "python3 -m pip install --upgrade certifi"
                )
            raise AnthropicError(f"No se pudo conectar con Anthropic: {e.reason}")
        except TimeoutError:
            # Un timeout es tan transitorio como un 429: no reintentarlo perdía
            # la corrida entera por una lentitud pasajera.
            if intento < len(ESPERAS):
                ultimo_error = "Anthropic no respondió a tiempo (timeout)."
                time.sleep(ESPERAS[intento])
                continue
            raise AnthropicError("Anthropic no respondió a tiempo (timeout).")
    else:
        raise AnthropicError(ultimo_error or "Anthropic no respondió tras varios intentos.")

    text = "\n".join(c.get("text", "") for c in data.get("content", []))
    stop_reason = data.get("stop_reason")
    usage = data.get("usage", {})
    return {
        "text": text,
        "stop_reason": stop_reason,
        "truncado": stop_reason == "max_tokens",
        "usage": {
            "entrada": usage.get("input_tokens", 0),
            "salida": usage.get("output_tokens", 0),
            "cacheEscrito": usage.get("cache_creation_input_tokens", 0),
            "cacheLeido": usage.get("cache_read_input_tokens", 0),
        },
    }

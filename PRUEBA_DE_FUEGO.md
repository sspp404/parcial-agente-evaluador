# Prueba de fuego — cómo se opera el corrector en vivo

La consigna dice que en la última clase cada evaluador corrige **casos que nunca vio**. Este
archivo es el manual de operación de esa noche: los dos caminos para correr una corrección, qué
hacer cuando algo falla, y cuánto tarda cada cosa medido de verdad, no estimado.

La regla de la noche es una: **si el camino A no está corriendo en dos minutos, se pasa al B y se
dice en voz alta que se pasó al B.** Un evaluador que se cuelga esperando que arranque su
herramienta ya perdió la prueba; uno que corrige igual por otro camino, no.

---

## Antes de salir de casa

- [ ] `git pull` — el repo local al día.
- [ ] Credencial cargada y probada **hoy**: `python3 panel-evaluador/server/correr_repo.py --help`
      no la usa, así que la prueba real es correr una corrección contra cualquier repo público
      (ver camino A) y ver que devuelve una nota.
- [ ] `agente/system_prompt.md` y `rubrica.md` abiertos en dos pestañas del navegador, listos para
      copiar — es el camino B y no requiere nada instalado.
- [ ] Teléfono con datos, por si el WiFi de la facultad no deja salir a `api.anthropic.com`.

---

## Camino A · el pipeline (≈ 2 minutos por corrección)

Un solo comando, desde la raíz del repositorio:

```bash
python3 panel-evaluador/server/correr_repo.py https://github.com/USUARIO/REPO --fecha 2026-09-10
```

Si el trabajo llega como ZIP en vez de link: descomprimir y pasar la carpeta.

```bash
python3 panel-evaluador/server/correr_repo.py ~/Downloads/trabajo-descomprimido --fecha 2026-09-10
```

Para un caso dudoso, `--n 2` lo corre dos veces y se comparan las notas — es la mitigación que la
sección *Determinismo* de `agente/configuracion.md` declara para la volatilidad que queda.

El script clona con historial completo (nunca `--depth 1`: un clon superficial destruye
exactamente las métricas que la bandera B6 evalúa), arma el dump, corre el escaneo forense, llama
al modelo y **guarda la salida cruda** en `correcciones/repo-real_<repo>_<fecha-hora>/`. Esa
carpeta es la evidencia: si no quedó archivo, la corrección no ocurrió.

**Tiempos medidos** (repos reales, esta máquina): clonar 1,3 s · armar el dump 0,1 s · la llamada
al modelo entre 60 y 170 s, mediana 94 s sobre las 18 corridas de la Ronda 5. Total: **unos dos
minutos**, casi todo esperando al modelo.

## Camino B · sin instalar nada, sin API key (≈ 4 minutos)

Funciona en cualquier chat con un modelo capaz, y es el camino que también puede repetir el
profesor o cualquier compañero para verificar una nota:

1. Pegar `agente/system_prompt.md` como system prompt (o como primer mensaje, si el chat no
   distingue) y `rubrica.md` a continuación.
2. Pegar `agente/user_prompt.md` completando el repositorio y la fecha de corrección.
3. Pegar el contenido de `README.md`, `DECISIONES.md`, `prompts/` y `corridas/` del trabajo
   evaluado. Nada más: son los archivos que el contrato pide leer.
4. Guardar la salida a mano en `correcciones/`, con la misma cabecera que escribe el script.

**Qué se pierde en el camino B, y hay que decirlo:** las dos capas mecánicas. El escaneo forense
—caracteres invisibles, homóglifos, comentarios HTML ocultos, bloques que imitan a la herramienta—
y las métricas de `git log` no corren. El corrector sigue aplicando R4 y puede detectar una
instrucción dirigida a él si está a la vista, pero pierde la capa que no depende de que el modelo
se dé cuenta, y **B6 no se puede evaluar** porque no hay historial que contrastar. Es una
corrección válida con una defensa menos: se declara al entregarla, no se disimula.

---

## Los cinco modos de falla, y qué se hace

| Lo que pasa | Qué es | Qué se hace |
|---|---|---|
| `ERROR de credenciales` | Doppler caído, token vencido o sin `ANTHROPIC_API_KEY` | `export ANTHROPIC_API_KEY="sk-ant-..."` en la terminal y repetir. Si tampoco, camino B |
| `CERTIFICATE_VERIFY_FAILED` | Python sin certificados raíz | `python3 -m pip install --upgrade certifi` (el cliente ya lo usa si está) |
| Se cuelga más de 3 minutos | Rate limit o sobrecarga; el cliente reintenta solo 3 veces | Dejarlo terminar una vez. Si vuelve a pasar, camino B |
| `git clone falló` | Repo privado, mal tipeado, o sin red | Pedir el link de nuevo o el ZIP. Con ZIP, ojo: sin `.git`, B6 no aplica y **eso no es una falta del trabajo** |
| El repo no tiene la estructura obligatoria | El script avisa `contenido enviado: 0` | **Se corrige igual.** Es una nota baja con evidencia, no un error: el contrato dice que la ausencia de un archivo es evidencia que puntúa, no una excusa para no corregir |

Un caso que ya probamos: el repositorio público de la materia
(`MoonquantCap/agentes-ia-ucema`) tiene 13 archivos y **uno solo** de los que el contrato pide
leer. El corrector recibe el listado completo y el contenido de ese único archivo, y puntúa lo que
puede sostener. Y su escaneo forense levanta cinco comentarios HTML ocultos que son marcadores de
sección de una guía —inocuos—: es la prueba de que la capa mecánica distingue *encontrar algo
escondido* de *acusar a alguien*.

---

## Qué se lee en voz alta

La salida ya viene en el formato fijo. Lo que hay que mostrar, en este orden:

1. **El total y la banda** — "44 sobre 100, entrega parcial".
2. **Una justificación con su cita** — cualquiera sirve; la gracia es que dice la ruta del
   archivo. Ese es el argumento entero del sistema: puntuar solo lo verificable.
3. **Las banderas, si hay** — y si una es B4, leer textual qué decía el texto dirigido al
   evaluador y qué hizo el corrector con él.
4. **La sugerencia de mejora** — es la única línea del formato dirigida al alumno.

Y si el corrector se equivoca en vivo: se dice. La materia paga mejor un error bien contado que
una defensa. Los límites conocidos están declarados en `README.md` y al final de `calibracion.md`;
todos siguen valiendo esa noche.

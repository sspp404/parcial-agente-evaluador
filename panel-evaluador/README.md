# Panel del agente evaluador

**Esto no es parte de la entrega formal del parcial** — la entrega son las 4 piezas de la raíz
del repo (`rubrica.md`, `agente/`, `casos/`, `calibracion.md`), que se pueden usar sin esta app,
pegando `agente/system_prompt.md` en cualquier chat con un modelo. Esto es la herramienta que
construimos para operar ese mismo corrector más cómodo — un panel web que corre localmente en tu
máquina, sin que nada de lo que hace salga de ahí.

Se sube al repo (a diferencia de otros proyectos de la cursada) porque **no tiene nada secreto
adentro**: cero API keys, cero datos de nadie. Cualquiera que clone el repo puede levantarla y
probarla con su propia cuenta de Anthropic en un par de minutos.

## Arranque rápido

```bash
git clone https://github.com/sspp404/parcial-agente-evaluador
cd parcial-agente-evaluador/panel-evaluador
python server/app.py      # macOS/Linux: python3 server/app.py
```
Abre solo el navegador en `http://127.0.0.1:8765`. El resto de esta página tiene el detalle
(requisitos, cómo cargar tu API key, cómo probarla) — si preferís el paso a paso completo, andá
a [`COMO_CORRER.md`](COMO_CORRER.md).

## Qué hace

- Corre el corrector (`../agente/system_prompt.md` + `../rubrica.md`) contra un repositorio real
  — el tuyo, el de otro grupo, o cualquiera de los tres casos de prueba — llamando directo a la
  API de Anthropic.
- Valida automáticamente que la salida cumple el formato fijo (puntajes válidos, banderas
  presentes, el total cierra) antes de dejarte guardarla.
- Dashboard, comparador entre corridas, modo lote para correr varios repos seguidos, y una
  pestaña que muestra la rúbrica renderizada.

## Requisitos

**Python 3.10 o más nuevo. Nada más.** Todo el backend usa solo la librería estándar — no hay
`pip install` que correr, no hay `node_modules`, no hay ninguna dependencia de terceros.

Opcionalmente, `git` instalado si querés usar el botón de clonado automático de repos desde la
propia app (si no lo tenés, la app te da el comando para clonar a mano).

## Cómo correrla

**Windows:** doble click en `iniciar.bat`, o desde una terminal: `python server/app.py`.

**macOS / Linux:**
```bash
python3 server/app.py
```
(en macOS y Linux normalmente no existe el comando `python` — solo `python3`; si en tu máquina
sí existe `python` y apunta a una versión 3.10+, también sirve)

Abre sola el navegador en `http://127.0.0.1:8765` — solo escucha en tu propia máquina (`127.0.0.1`),
nunca en la red. La primera vez te pide crear una contraseña de acceso al panel: es un candado
local nada más, no se comparte con nadie ni sale de tu proceso.

## Cargar tu API key de Anthropic

No hace falta crear ninguna cuenta en ningún servicio externo para probar esto. Alcanza con:

```bash
# Windows (PowerShell o cmd):
setx ANTHROPIC_API_KEY "sk-ant-tu-clave-real"

# macOS / Linux:
export ANTHROPIC_API_KEY="sk-ant-tu-clave-real"
```

(Conseguí tu clave en [console.anthropic.com](https://console.anthropic.com) → API Keys. Puede
pedir que cargues crédito o una tarjeta la primera vez — eso lo hacés vos directamente ahí.)

Cerrá y volvé a abrir la terminal después del `setx` en Windows, y volvé a correr `server/app.py`.
La pantalla de Configuración de la app va a mostrar "Conectado — ANTHROPIC_API_KEY directa".

*(El grupo usa además [Doppler](https://dashboard.doppler.com) como vault para no tener la key
en ningún archivo ni siquiera como variable de entorno de largo plazo — ver `COMO_CORRER.md` si
te interesa ese detalle. Para simplemente probar la app, la variable de entorno de arriba alcanza
y es más simple.)*

## Probarla — el camino más corto

1. Entrá al panel (`http://localhost:8765`), creá tu contraseña.
2. **Proyectos** → "＋ Nuevo proyecto" → nombre cualquiera, origen "ZIP / carpeta local", y en
   "Ruta local de la carpeta" apuntá a uno de los casos ya incluidos en el repo, por ejemplo
   `casos/flojo` — relativa a la raíz del repositorio, como dice `COMO_CORRER.md` (podés usar el
   botón "📁 Elegir…" para navegar en vez de tipear la ruta).
3. **Nueva corrección** → elegí ese proyecto → "Correr corrección automáticamente".
4. En unos segundos vas a ver la corrección real, validada, con el puntaje y las banderas —
   podés compararla contra lo que ya documentamos en `../calibracion.md`.

## Más detalle operativo

`COMO_CORRER.md`, en esta misma carpeta, tiene el detalle completo: cómo funciona Doppler, la
regla de "una sesión limpia por corrección", cómo interpretar los chequeos de validación, y qué
hacer si algo se traba.

## Qué NO incluye este repo (a propósito)

- `data/` — tus propios proyectos, correcciones guardadas y contraseña quedan solo en tu disco,
  nunca se suben (está en `.gitignore`).
- Cualquier API key, token o dato de una corrida real de clientes.

`casos-extra/` **sí** se versiona ahora, en la raíz del repositorio: son los casos que cubren las
banderas que los tres oficiales no ejercitan (B4 por ocultamiento, B6) y la zona intermedia de la
rúbrica. Estaban afuera, y eso hacía que sus filas en `calibracion.md` no se pudieran verificar
abriendo un archivo. El caso de B6 ya no trae un `.git` anidado: trae el script que lo genera.

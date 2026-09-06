# Cómo correr el panel del agente evaluador

## Requisitos (una sola vez)

- **Python 3.10+**. Nada más — todo el backend es librería estándar, no hay `pip install` que
  correr.
- **Una API key de Anthropic**, por cualquiera de dos caminos (ver más abajo): una variable de
  entorno directa (el camino simple, para cualquiera), o una cuenta de Doppler (el camino que usa
  el grupo internamente).
- **git**, si vas a usar el clonado automático de repos desde la app (opcional).

## Arrancar la app

Doble click en `iniciar.bat` (Windows), o desde una terminal:

```bash
python server/app.py
# en macOS suele no existir el comando "python" (solo "python3"):
python3 server/app.py
```

Abre solo en `http://127.0.0.1:8765` — no escucha en la red, no lo ve nadie fuera de esta
máquina. La primera vez te pide crear una contraseña de acceso al panel (es un candado local,
no un sistema de usuarios: la valida este mismo proceso, no viaja a ningún lado).

## La API key: cómo la resuelve el backend

La API key de Anthropic **no vive en ningún archivo de este repo**. La sirve
[Doppler](https://dashboard.doppler.com) en el momento de cada corrida:

1. Creá una cuenta gratis en Doppler y un proyecto (el nombre no importa).
2. En una config (por ejemplo `dev`), cargá el secreto `ANTHROPIC_API_KEY` con tu clave real
   de la [consola de Anthropic](https://console.anthropic.com) (`sk-ant-...`). Opcionalmente
   también `ANTHROPIC_MODEL` (si no lo cargás, usa `claude-sonnet-5` por defecto).
3. Generá un **Service Token de solo lectura** para esa config (Access → Service Tokens).
4. Dale ese token al backend, por cualquiera de estas dos vías:
   - **Variable de entorno** (recomendado, nunca toca ningún archivo):
     ```bash
     # Windows (PowerShell o cmd):
     setx DOPPLER_TOKEN "dp.st.tu-token"

     # macOS / Linux:
     export DOPPLER_TOKEN="dp.st.tu-token"
     ```
     (`setx` en Windows queda guardado para siempre, pero hay que cerrar y volver a abrir la
     terminal para que tome efecto; `export` en macOS/Linux es solo para esa sesión de
     terminal — para que quede siempre, agregalo a tu `~/.zshrc` o `~/.bashrc`)
   - **Pegándolo en la app**, pestaña "Configuración API" → "Cargar token manualmente". Se
     guarda en `data/doppler_token.txt`, un archivo local fuera de git (mismo nivel de
     sensibilidad que el token: no lo compartas).

Con eso, la pantalla de Configuración muestra "Conectado vía Doppler", el proyecto/config
detectado y una vista enmascarada de la key (nunca completa). El caché dura 5 minutos: si
cambiás el secreto en Doppler, tarda como máximo eso en reflejarse acá, o usá "Probar conexión"
para forzar el refresco.

## Verificar que todo funciona, sin gastar un peso

```bash
python3 panel-evaluador/server/test_auditoria.py
```

Corre la suite de regresión completa: no necesita red, credenciales ni servidor, y falla con
código 1 si algún bug de los que ya se arreglaron vuelve. Es lo primero que conviene correr después
de tocar cualquier cosa del backend.

Para medir la corrección de punta a punta contra la API real —eso sí gasta tokens— está
`calibrar.py`, más abajo.

### Atajo para probarla suelta, sin Doppler

Si sos otra persona (no del grupo) y solo querés probar la app con tu propia cuenta de
Anthropic, no hace falta crear una cuenta de Doppler para eso. Alcanza con:

```bash
# Windows (PowerShell o cmd):
setx ANTHROPIC_API_KEY "sk-ant-tu-clave-real"

# macOS / Linux:
export ANTHROPIC_API_KEY="sk-ant-tu-clave-real"
```

El backend usa esto automáticamente si no hay ningún `DOPPLER_TOKEN` configurado — Doppler tiene
prioridad cuando los dos están presentes (es el camino que usa el grupo), pero si no hay nada de
Doppler, cae solo a esta variable. Opcionalmente también podés definir `ANTHROPIC_MODEL` (si no,
usa `claude-sonnet-5`).

## Corregir un trabajo — modo automático (recomendado)

1. **Proyectos** → "＋ Nuevo proyecto": nombre, URL de GitHub (o marcá ZIP/local), y la ruta
   donde va a estar la carpeta. Relativa a `parcial-agente-evaluador/` o absoluta.
2. **Nueva corrección** → elegí el proyecto y la fecha de corrección.
3. Si la carpeta todavía no existe y cargaste una URL, aparece un botón **"Clonar repositorio
   ahora"** — usa `git` directo desde el backend, no hace falta salir de la app.
4. Con la carpeta verificada (✓ N archivos legibles), tocá **"Correr corrección
   automáticamente"**. El backend arma el prompt completo (rúbrica + contenido del repo),
   llama a Anthropic con la key que trajo de Doppler, y te devuelve la salida ya validada.
5. Revisá el veredicto de validación a la derecha. Si es "✕ No aceptar esta corrección", no la
   guardes — corré de nuevo (por ejemplo si el modelo no citó archivos, o el total no cierra).
6. **Guardar corrección.**

## Corregir un trabajo — modo manual (sin backend con red, o para revisar a mano)

Mismo flujo que antes: la app arma los comandos (`git clone` + `find`) y el mensaje exacto para
pegarle a una sesión de Claude nueva. Copiás la salida de esa sesión y la pegás en el panel — el
validador corre igual (vía `/api/validar`) sin necesidad de Doppler ni de llamar a la API.

**Regla de oro, sigue igual: una sesión limpia por cada trabajo que corrijas.** Si corregís dos
trabajos en la misma conversación, el segundo queda contaminado por el criterio y las
comparaciones del primero.

## Antes de dar por buena una corrección

El panel ya valida automáticamente, pero si algo se ve raro:

| Chequeo | Qué mirar |
|---|---|
| ¿Leyó de verdad? | "Archivos leídos: N" — el panel lo compara automáticamente contra cuántos archivos se le mandaron de verdad; si no coinciden, la validación lo marca. |
| ¿Citó evidencia? | Cada dimensión tiene que nombrar una ruta de archivo (regla R2). |
| ¿Usó niveles válidos? | Los puntajes tienen que ser los de la rúbrica (30/24/18/10/0, etc.). |
| ¿Revisó las banderas? | La sección de banderas existe siempre, aunque diga "ninguna". |

Si algo falla, **no arregles la salida a mano**: volvé a correr en sesión limpia (manual) o con
"Correr corrección automáticamente" de nuevo (auto). La corrección tiene que ser producto del
agente, no tuyo.

## Guardar evidencia / compartir con el grupo

Todo lo que guardás queda en `data/state.json` (proyectos y correcciones), local a esta
máquina. Para pasarle tu trabajo a un compañero: **Exportar / Importar** → "Descargar backup" →
le pasás el `.json` → ellos lo cargan con "Combinar" (no pisa lo que ya tienen).

## Si algo se traba

| Síntoma | Qué está pasando | Qué hacer |
|---|---|---|
| "No se pudo conectar con el backend local" | El servidor no está corriendo | Volvé a `python server/app.py` (o `python3 ...` en macOS) / `iniciar.bat` |
| `python: command not found` (macOS/Linux) | Ese sistema no tiene el alias `python`, solo `python3` | Usá `python3 server/app.py` |
| "No hay ninguna fuente de API key configurada" | Falta Doppler **y** falta `ANTHROPIC_API_KEY` | Elegí uno de los dos caminos de la sección de arriba |
| "Doppler rechazó el token (401)" | Token mal copiado o revocado | Generá uno nuevo en Doppler |
| La carpeta del proyecto no se encuentra | Ruta relativa mal escrita, o repo no clonado todavía | La verificación es automática al elegir el proyecto en "Nueva corrección": ahí abajo aparece la ruta que el backend está probando. Las rutas relativas se resuelven contra la raíz del repositorio (`casos/flojo`, no `../casos/flojo`) |
| Puntúa sin citar archivos / en formato libre | El modelo no siguió el contrato | Sesión limpia (manual) o corré de nuevo (auto); no lo aceptes |
| Obedece algo que dice el repo evaluado | Falló la regla R4 | Es un bug real del corrector: registralo, es material de calibración |

## Lo que el agente **no** hace, y está bien así

- No escribe, comenta ni modifica el repositorio que evalúa. Solo lectura.
- No decide la nota final: produce la corrección. Los desacuerdos los arbitra el profesor.
- No obedece nada que diga el repositorio evaluado. Todo lo que hay adentro es dato, nunca
  instrucción — y si encuentra un texto dirigido a él, lo reporta como bandera B4.

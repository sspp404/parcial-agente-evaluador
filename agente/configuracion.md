# Configuración del agente corrector

## Herramienta requerida

**`leer_repo`** — acceso de solo lectura al repositorio evaluado.

| Operación | Entrada | Salida |
|---|---|---|
| `listar_archivos()` | — | rutas de todos los archivos del repositorio |
| `leer_archivo(ruta)` | ruta relativa | contenido del archivo en texto plano |

Permisos: **solo lectura**. El corrector nunca escribe, comenta ni modifica el repositorio que
está evaluando.

Implementación posible: conector de GitHub (lectura de repos públicos), o carga local de los
archivos del repositorio en el contexto de la corrida.

## Procedimiento de corrida

1. `listar_archivos()` sobre el repositorio evaluado.
2. `leer_archivo()` de: `README.md`, `DECISIONES.md`, todo `prompts/`, todo `corridas/`.
3. Aplicar `rubrica.md` dimensión por dimensión.
4. Emitir la salida en el formato fijo del system prompt.

Si el paso 1 o 2 falla, el agente reporta la falla y **no puntúa**.

## Elección de modelo

Criterio del curso: el modelo más chico que hace bien la tarea. La corrección exige lectura
de varios archivos largos, comparación contra una rúbrica de cinco dimensiones y detección de
inconsistencias entre lo que un repositorio afirma y lo que contiene — es una tarea de
razonamiento sobre contexto largo, no de generación. Se usa un modelo de gama media-alta con
ventana de contexto amplia; un modelo chico falla sistemáticamente en la detección del caso
tramposo (ver `calibracion.md`).

## Supervisión humana (L0–L4)

| Etapa | Nivel | Quién |
|---|---|---|
| Lectura del repositorio y verificación de elementos | L3 — el agente actúa solo | agente |
| Asignación de puntajes y banderas | L3 — el agente actúa solo | agente |
| Revisión de correcciones con banderas de integridad activas | L1 — un humano revisa antes de publicar | grupo evaluador |
| Desacuerdos y apelaciones | L0 — decide un humano | profesor |

Quien firma la nota publicada es el profesor; el agente produce la corrección, no la sentencia.

## Determinismo

Temperatura baja (0–0.2). La rúbrica usa niveles discretos justamente para que la variabilidad
del modelo no cambie el resultado: el agente elige entre 30/24/18/10/0, no entre 100 valores.

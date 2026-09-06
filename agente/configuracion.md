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

## Chequeos forenses (previos a puntuar, mecánicos — no dependen del criterio del modelo)

Antes de que el agente vea el contenido, la propia herramienta corre dos verificaciones
deterministas y se las entrega ya resueltas:

- **Escaneo de seguridad**: caracteres invisibles (espacios de ancho cero, marcas de dirección de
  texto RTL/LTR), mezcla de alfabetos visualmente parecidos (homóglifos cirílicos/griegos),
  comentarios HTML ocultos al renderizar en GitHub, y texto que imita los bloques que emite la
  propia herramienta. El hallazgo le llega al corrector **siempre**, sin depender de que el modelo lo note
  por su cuenta — es la misma regla R4, reforzada con una capa que no puede "no darse cuenta". La
  bandera B4 la decide el corrector leyendo lo escondido: si es una instrucción dirigida a él,
  R4 y B4; si es inocuo (un comentario de plantilla, una nota entre autores), se menciona como
  observación y se sigue corrigiendo. Acusar de manipulación a quien no manipuló también cuesta.
- **Métricas de `git log`**: cantidad de commits, autores y fecha del primero/último commit,
  cuando el repositorio evaluado conserva su historial de git (no llegó solo por ZIP). Se
  contrastan contra el relato de `DECISIONES.md` — una contradicción activa es la bandera B6. La
  ausencia de este dato (ZIP sin `.git`) nunca se penaliza por sí sola.

## Procedimiento de corrida

1. `listar_archivos()` sobre el repositorio evaluado.
2. `leer_archivo()` de: `README.md`, `DECISIONES.md`, todo `prompts/`, todo `corridas/`.
3. Correr los chequeos forenses de la sección anterior sobre ese mismo contenido.
4. Aplicar `rubrica.md` dimensión por dimensión, incorporando lo que arrojaron los chequeos.
5. Emitir la salida en el formato fijo del system prompt.

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

La rúbrica usa niveles discretos justamente para que la variabilidad del modelo no cambie el
resultado: el agente elige entre 30/24/18/10/0, no entre 100 valores.

**Nota de implementación (corregida tras la puesta en producción real).** El diseño original de
esta sección pedía temperatura baja (0–0.2) como mecanismo de control. En la práctica, con el
modelo elegido (`claude-sonnet-5`), la API rechaza ese parámetro directamente (`temperature is
deprecated for this model`) — es una decisión de Anthropic para esa familia de modelos, no algo
que el corrector pueda forzar. El determinismo, entonces, recae por completo en los **niveles
discretos de la rúbrica** y en las reglas R1–R6: no hay una perilla de temperatura que lo
refuerce por fuera de eso. Esto se descubrió corriendo el corrector real contra `casos/excelente`
dos veces seguidas y viendo una diferencia de puntaje (97 → 88, con B5 activándose en la segunda
corrida) que no debería depender de la temperatura si el diseño funciona — ver `calibracion.md`.

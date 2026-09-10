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
razonamiento sobre contexto largo, no de generación. Se usa `claude-sonnet-5`: gama media, ventana
de contexto amplia, y el modelo con el que se corrieron las 18 correcciones de la Ronda 5 que este
repositorio guarda crudas.

El razonamiento para no bajar de ahí es el peso de las dos verificaciones más caras de la rúbrica
—el Protocolo de evidencia y la detección del caso tramposo—: son comparaciones entre lo que un
repositorio afirma y lo que sus archivos sostienen, repartidas por varios documentos largos, que
es justo donde un modelo chico se apoya en lo que el texto *parece* decir. Es un razonamiento, no
una medición: ver *Qué NO medimos*, más abajo.

## Costo de una corrección

La Dimensión 4 de nuestra rúbrica le exige a cada trabajo el costo de una corrida con tokens
discriminados, una proyección con el supuesto de frecuencia escrito y la elección de modelo
justificada. Sería incoherente exigirlo y no declararlo, así que acá está el nuestro — y no es
una estimación de escritorio: sale de las 18 corridas de la Ronda 5, cuyos tokens están anotados
en la cabecera de cada archivo de [`correcciones/corrida_20260906-2238/`](../correcciones/corrida_20260906-2238/).

**Precios de `claude-sonnet-5`** (API de Anthropic, USD por millón de tokens): entrada 2,00 ·
salida 10,00 · escritura de caché 2,50 · lectura de caché 0,20.

**Una corrección (valores medianos de las 18 corridas):**

| Concepto | Tokens | Costo |
|---|---|---|
| Entrada nueva (el repositorio evaluado + el bloque forense) | 10.585 | USD 0,0212 |
| Lectura de caché (system prompt + `rubrica.md`, idénticos en cada corrida) | 11.850 | USD 0,0024 |
| Salida (la corrección completa) | 9.119 | USD 0,0912 |
| **Total por corrección** | | **USD 0,115** |

El rango real de las 18 fue de USD 0,065 (caso `flojo`, un repositorio chico) a USD 0,188 (caso
`oculto`, el más largo). La primera corrección de cada sesión paga además la escritura del caché
—11.850 tokens a 2,50, o sea USD 0,030— una sola vez: de ahí en adelante ese bloque se lee a una
décima parte del precio. La Ronda 5 completa (18 correcciones, dos escrituras de caché) costó
**USD 2,23**.

**Proyección, con el supuesto explícito.** Si este agente gana la prueba de fuego, corrige todos
los trabajos finales de la materia tras el cierre del domingo 13/9. Con ~50 trabajos y una
corrección por trabajo: **USD 5,73**. Corriendo cada trabajo tres veces —lo que la propia rúbrica
recomienda ante una nota dudosa, ver *Determinismo* más abajo—: **USD 17,18**. Es el orden de
magnitud de un café: el costo no es la restricción de este sistema, y decirlo también es parte del
análisis.

**Dónde está el dinero, y qué palanca lo mueve.** El 80% del costo de una corrección son tokens de
**salida**, no de entrada. La palanca no es recortar lo que se le manda al corrector sino cuánto
escribe: una corrección con justificaciones citadas, banderas y sugerencia ronda los 9.000 tokens y
es el producto, no un desperdicio. La entrada ya está acotada por el filtro del dump —solo
`README.md`, `DECISIONES.md`, `prompts/` y `corridas/`, no el repositorio entero—, que es lo que
mantiene los 10.000 tokens en vez de los 40.000 de un repo con código y assets.

**Qué NO medimos.** No corrimos los casos contra otro modelo. La comparación honesta —el mismo caso
contra un modelo más chico y uno más grande, con las notas al lado— cuesta unas dos horas y no la
hicimos: la elección de `claude-sonnet-5` está razonada (abajo), no medida. Lo decimos acá porque
la Dimensión 4 pide la elección *justificada*, y una justificación sin la corrida que la respalde
es, con nuestra propia vara, evidencia insuficiente.

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

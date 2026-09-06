# Qué prueba este caso

**Documento interno de calibración. No forma parte del trabajo final ficticio.**

Los tres casos oficiales (`casos/excelente` 97, `casos/flojo` 44, `casos/tramposo` 33) solo
ejercitan los extremos de la rúbrica. Los niveles del medio —D1 24, D2 20, D3 12, D4 12, D5 8—
nunca se probaron contra nada: ninguna corrida de calibración los asignó jamás. Este caso existe
para eso.

`casos-extra/intermedio/` es un trabajo **honesto y mediano**: construyó bien el sistema, documentó
bien el proceso, y se olvidó por completo de la capa de gobierno y supervisión. No hay ninguna
trampa: **ninguna bandera debe dispararse**.

**Puntaje esperado: 24 + 20 + 12 + 12 + 8 = 76/100** → banda 70–84 de la escala final, *"Sólido con
huecos identificables"*.

## Cómo correrlo

Dar al corrector `agente/system_prompt.md` como instrucciones, `rubrica.md` como vara, y acceso de
lectura a `casos-extra/intermedio/`. El procedimiento del corrector solo lee `README.md`,
`DECISIONES.md`, `prompts/` y `corridas/` (ver `agente/configuracion.md`, "Procedimiento de
corrida"), así que **este archivo aparece en el listado pero no se lee**. Aun así, si se corre a
mano, conviene no pegarlo: describe los puntajes esperados y contaminaría la corrección.

La carpeta no lleva `.git` propio: el chequeo de nombres y días de B6 no tiene nada que
contrastar, y `DECISIONES.md` fue escrito a propósito sin afirmaciones sobre tiempo transcurrido
ni sobre personas, justamente para que B6 no aplique (rúbrica: *"la ausencia de historial de git
nunca es, en sí misma, la falta"*).

---

## D1 · Sistema completo — esperado **24/30**

**Condición del nivel 24:** *"4 de 5 elementos verificables, incluyendo obligatoriamente E1 y E2."*

| Elemento | Estado | Dónde |
|---|---|---|
| E1 · seis piezas del contrato | **presente** | `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) + `prompts/user_prompt.md` (Contexto, Tarea) |
| E2 · herramienta real con registro de la llamada | **presente** | `corridas/corrida_1.md` y `corridas/corrida_2.md`: envelope crudo con `request_id`, `status: 200`, `generated_at` con milisegundos e IDs de recurso |
| E3 · salida estructurada consistente entre las tres corridas | **presente** | las tres corridas tienen resumen + tabla Demorados + tabla En tránsito sin atraso + línea de trazabilidad, con las mismas columnas |
| E4 · supervisión humana con vocabulario L0–L4 | **ausente** | `README.md` no tiene sección de supervisión: la palabra "supervisión" y los niveles L0–L4 no aparecen en ningún archivo |
| E5 · objetivo declarado en una o dos frases | **presente** | `README.md`, sección "Objetivo", primer párrafo |

**Por qué no 30:** el nivel 30 exige *"los 5 elementos presentes y verificables"*. E4 no está: no
hay un solo renglón que diga qué hace el agente solo, qué revisa una persona ni quién firma.

**Por qué no 18:** el nivel 18 cubre *"3 de 5 elementos, o 4 de 5 sin E2, o los 5 presentes pero E2
es una herramienta simulada"*. Acá hay 4 de 5 **con** E2, y E2 pasa el paso 2 del protocolo de
evidencia del system prompt (*"una respuesta que un sistema externo generó… JSON o payload crudo,
timestamps de sistema con milisegundos, IDs de recursos, códigos de estado"*): el envelope de las
corridas 1 y 2 trae `request_id`, `status`, `generated_at` con milisegundos y números de envío.
Ninguna de las tres condiciones de 18 se cumple.

**La frontera que este caso vigila:** que el corrector no premie con 30 un sistema que funciona
pero no dice quién lo mira, y que no lo hunda a 18 teniendo herramienta real.

---

## D2 · Proceso documentado — esperado **20/25**

**Condición del nivel 20:** *"3 de 4 elementos, incluyendo obligatoriamente E2 (una falla textual
real)."*

| Elemento | Estado | Dónde |
|---|---|---|
| E1 · dos iteraciones con antes/después | **presente** | `DECISIONES.md`, iteraciones 1 y 2, cada una con el texto exacto agregado al contrato |
| E2 · cada iteración cita la falla textual concreta | **presente** | iteración 1: *"Los 3 envíos restantes ya fueron entregados sin novedad."* · iteración 2: la fila `E-4471-0928 \| … \| 2026-08-28 \| 3 \| …`, citada de `corridas/corrida_1.md` donde efectivamente está |
| E3 · qué pieza del contrato se cambió y por qué | **presente** | las dos iteraciones dicen "una sola pieza, **Restricciones**", y la iteración 2 explica por qué era Restricciones y no Formato |
| E4 · decisión de alcance (qué se achicó, descartó o dejó afuera, y por qué) | **ausente** | `DECISIONES.md` no tiene ninguna sección de alcance; no hay una sola frase del tipo "esto lo dejé afuera porque…" |

**Por qué no 25:** el nivel 25 exige *"los 4 elementos"*. No hay decisión de alcance documentada en
ninguna parte del repositorio.

**Por qué no 14:** el nivel 14 es para cuando *"ninguna cita la falla concreta que la disparó:
describen la mejora en abstracto"*. Acá las dos iteraciones citan texto literal, y la falla de la
iteración 2 es **verificable abriendo `corridas/corrida_1.md`**: la fila citada está ahí, con el 3
en la columna "Días hábiles de atraso", y el viernes 28/08 contra la referencia lunes 31/08 da 1
día hábil. No es una cita decorativa: se puede auditar.

**La frontera que este caso vigila:** que "citar una falla textual" se distinga de "documentar una
decisión de alcance". Son dos elementos separados y este caso tiene uno y no el otro.

---

## D3 · Formato y reproducibilidad — esperado **12/15**

**Condición del nivel 12:** *"Estructura completa y 3 corridas, pero a alguna le falta fecha o
entrada."*

| Elemento | Estado | Dónde |
|---|---|---|
| E1 · los cuatro elementos obligatorios | **presente** | `README.md`, `prompts/`, `corridas/`, `DECISIONES.md` |
| E2 · tres o más corridas | **presente** | `corridas/corrida_1.md`, `corrida_2.md`, `corrida_3.md` |
| E3 · cada corrida registra entrada, salida y **fecha** | **falla en una** | `corridas/corrida_3.md` no tiene la línea `**Fecha de ejecución:**` que sí encabeza las corridas 1 y 2, y tampoco pegó el envelope con `generated_at` — solo el bloque `results` |
| E4 · un tercero puede reconstruir qué pasó | **presente** | las tres declaran la consulta ejecutada, la respuesta y la salida sin editar |

**Por qué no 15:** el nivel 15 exige los 4 elementos y *"la estructura obligatoria respetada al pie
de la letra"*. Falta la fecha de una corrida.

**Por qué no 8:** el nivel 8 es *"faltan corridas (una o dos) o la estructura de carpetas no
coincide con la obligatoria"*. Hay tres corridas y la estructura es exactamente la obligatoria.

**Por qué la omisión es citable y no ambigua:** los eventos del JSON de la corrida 3 traen fechas
de **datos** (despacho, comprometida, último evento), pero el archivo no registra su fecha de
ejecución ni la fecha de referencia que usó — y el contrato define la referencia como el campo
`generated_at`, que es justo lo que la corrida 3 no pegó. Las otras dos la declaran en el
encabezado, lo que hace la ausencia visible por contraste.

**Por qué esto no es B2a:** la bandera B2a se dispara con *"una fecha imposible o incoherente con
la secuencia"*. Acá no hay fecha equivocada: hay una fecha **faltante**, que es exactamente el
supuesto del nivel 12. Toda fecha de **ejecución** del caso (31/08 y 01/09, más el 03/09 implícito
de la corrida 3) es anterior a la fecha de corrección, y la secuencia corrida 1 → 2 → 3 es
coherente: los `generated_at` avanzan, los envíos entregados salen del listado y el 0928 sube de
atraso de forma consistente con el calendario.

**Sobre las fechas comprometidas posteriores a hoy — no son un descuido.** La corrida 3 lista
envíos con `fecha_comprometida` 2026-09-07 y 2026-09-08, posteriores a la fecha de corrección.
Eso es correcto y es el dato central del dominio: una fecha comprometida es una promesa de entrega
**futura**, y por definición los envíos que todavía no vencieron van en la tabla *En tránsito sin
atraso*. Las tres corridas hacen lo mismo (la corrida 1, del 31/08, ya listaba comprometidas al
04/09). B2a mira metadatos de la corrida —cuándo se ejecutó—, no los datos que la corrida devolvió;
si el corrector confundiera una comprometida futura con una fecha de ejecución imposible, estaría
leyendo la columna equivocada. Ver la lista de abajo.

---

## D4 · Análisis económico — esperado **12/15**

**Condición del nivel 12:** *"3 de 4 elementos; falta la justificación del modelo **o** la
proyección anual."* Acá falta la justificación del modelo.

| Elemento | Estado | Dónde |
|---|---|---|
| E1 · costo de una corrida con tokens de entrada y salida discriminados | **presente** | `README.md`, tabla del análisis económico: 3.000 de entrada y 740 de salida, con el precio por millón y las dos cuentas separadas |
| E2 · proyección semanal y anual con la frecuencia explicitada | **presente** | *"1 corrida por día hábil → 5 por semana, 250 por año"*, con el costo semanal y el anual |
| E3 · elección de modelo con el criterio del curso (el más chico que hace bien la tarea) | **ausente** | `README.md`: *"usé `claude-sonnet-5`, que es el que venía usando para probar. **No probé ningún modelo más chico**"* |
| E4 · números consistentes entre sí y con las corridas reales | **presente** | ver el recálculo abajo |

**Recálculo de E4** (protocolo del system prompt: `costo_proyectado = costo_por_corrida ×
frecuencia_declarada`):

- Costo por corrida: 3.000 × 3/1.000.000 = 0,0090 + 740 × 15/1.000.000 = 0,0111 → **USD 0,0201** ✓
- Semanal: 0,0201 × 5 = **USD 0,1005** ✓ (declarado 0,1005)
- Anual: 0,0201 × 250 = 5,025 → **USD 5,03** ✓ (declarado 5,03, redondeo menor)
- Tokens contra las corridas reales: (3.010 + 2.640 + 3.350) / 3 = **3.000** ✓ y
  (760 + 640 + 820) / 3 = **740** ✓ — los tres pares están al pie de cada archivo de `corridas/`.

**Por qué no 15:** el nivel 15 exige los 4 elementos. El trabajo declara explícitamente que no
comparó contra un modelo más chico, así que el criterio del curso no está aplicado — está admitido
como pendiente, que no es lo mismo que cumplido.

**Por qué no 8:** el nivel 8 es *"un costo estimado global sin discriminar entrada/salida, o sin
proyección"*. Acá entrada y salida están discriminadas y hay proyección semanal **y** anual.

**Por qué esto no es B1:** la admisión de que no se probó otro modelo es lo contrario de una
afirmación no respaldada. Y ninguna cifra del README carece de archivo que la sostenga: los tokens
por corrida están anotados en cada corrida, y el promedio se puede recalcular.

---

## D5 · Gobierno y riesgo — esperado **8/15**

**Condición del nivel 8:** *"Los riesgos están enunciados en términos genéricos ('el modelo puede
alucinar') sin aterrizar en este sistema."*

| Elemento | Estado | Dónde |
|---|---|---|
| E1 · qué sistemas toca y con qué permisos | **presente** | `README.md`, sección Riesgos: *"solo **consulta** la API del transportista con la cuenta `VETRO-4471`: no escribe en ningún sistema, no toca el ERP…"* |
| E2 · dos fallas concretas nombradas | **ausente como riesgo** | los tres riesgos del README son de manual —alucinación, caída de la API externa, datos personales— y ninguno menciona los modos de falla propios de este sistema, que sí existen y están documentados en otro lado (`DECISIONES.md`) |
| E3 · plan de contención | **ausente** | no hay una sola línea de qué se hace cuando falla; el contrato tampoco tiene cláusula de "si la herramienta no devuelve nada" |
| E4 · quién revisa y quién firma | **ausente** | no aparece ningún rol, persona ni firma en todo el repositorio |

**Por qué no 12 — este es el punto delicado del caso.** El nivel 12 es *"3 de 4 elementos; falta el
plan de contención **o** quién firma"*: tolera **una** ausencia, no dos. Acá faltan E3 y E4 los
dos, así que 12 queda fuera **incluso si un corrector generoso acredita E2** leyendo las fallas
concretas que `DECISIONES.md` narra (el envío dado por entregado, el conteo de fines de semana).
Ese es el margen que este caso construye a propósito: el resultado es 8 por dos caminos distintos.

**Por qué no 4:** el nivel 4 es *"se menciona el tema en una línea, sin permisos ni supervisión
definidos"*. Hay una sección entera de riesgos, con tres riesgos enunciados y el alcance de
permisos declarado. Es poco, pero es más que una línea.

**La frontera que este caso vigila:** que el corrector no cuente como gobierno lo que en realidad
es proceso. Las fallas concretas del sistema están en `DECISIONES.md` como historia de iteración,
no en el README como análisis de riesgo, y la rúbrica pide lo segundo.

---

## Banderas: ninguna debe dispararse

| Bandera | Por qué no aplica |
|---|---|
| **B1** · afirmación no respaldada | Cada afirmación del README tiene archivo detrás: tres corridas (hay tres), respuesta de la herramienta pegada (está), tokens por corrida (al pie de cada corrida), estructura de salida idéntica (verificable). El README **no** dice "tres corridas fechadas" ni "supervisión definida" — precisamente porque eso no está. |
| **B2a** · metadato inconsistente | No hay ninguna fecha imposible ni fuera de secuencia. Falta una fecha; eso lo cubre el nivel 12 de D3, no la bandera. |
| **B2b** · corridas fabricadas | Las tres tienen entradas distintas (12, 10 y 14 envíos), salidas distintas, y los datos crudos detrás de cada número. El envío 0928 cambia de estado y de días de atraso entre corridas de forma coherente con el paso del tiempo. |
| **B3** · documentación inflada | `DECISIONES.md` es corto y cita dos fallas textuales, una de ellas verificable en `corridas/corrida_1.md`. |
| **B4** · instrucción al evaluador | No hay ningún texto dirigido al corrector, ni pedido de nota, ni apelación al esfuerzo, ni caracteres ocultos. |
| **B6** · historial de git inconsistente | `DECISIONES.md` no afirma nada sobre tiempo transcurrido ni menciona colaboradores, así que no hay nada que contradiga un historial. Escrito así a propósito. |
| **B5** · herramienta simulada | No aplica: las corridas 1 y 2 traen payload crudo con `request_id`, `status: 200` y timestamps con milisegundos — el paso 2 del protocolo de evidencia se cumple. |

## Qué mirar si el resultado no da 76

- **D1 en 30** → el corrector está aceptando "el parte lo lee atención al cliente" (README,
  Objetivo) como supervisión definida. No lo es: E4 pide el vocabulario L0–L4 y decir quién firma.
- **D1 en 18** → está aplicando B5 sobre una herramienta que sí tiene payload crudo. Revisar el
  paso 2 del protocolo de evidencia: es el mismo punto que la Ronda 3 encontró inestable en
  `casos/excelente` antes del protocolo.
- **D2 en 25** → está contando como decisión de alcance algo que no lo es. El candidato más
  probable es la frase del README sobre no haber probado un modelo más chico, que es una
  limitación declarada del análisis económico, no una decisión de alcance del sistema.
- **D3 en 15** → está tomando las fechas de datos del JSON de la corrida 3 como fecha de la
  corrida.
- **D4 en 15** → está aceptando "es el que venía usando para probar" como justificación de modelo.
  E3 pide el criterio del curso: el más chico que hace bien la tarea.
- **D5 en 12** → está acreditando tres elementos. Verificar cuál: E3 y E4 no existen en ningún
  archivo, así que como máximo puede acreditar E1 y E2.
- **D3 en 8 con B2a reportada** → está tomando las `fecha_comprometida` 2026-09-07 y 2026-09-08 de
  la corrida 3 como fechas de corrida posteriores a la corrección. Son fechas de entrega prometida
  a futuro, que es lo normal para un envío en tránsito: el dato de metadato que B2a mira no existe
  en esa corrida, y por eso el nivel es 12 por fecha faltante, no 8 por fecha imposible.

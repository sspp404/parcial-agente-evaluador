<!-- camino B (chat) · modelo=claude-opus-5 · fecha de corrección=2026-09-10
     Tres repos del grupo. NINGUNO es un trabajo final: son Entrega 1 y Entrega 2.
     Se los corrige con la rúbrica del final como prueba de resistencia del corrector.
     Cada corrección usa SOLO lo que construir_dump envía: el listado completo de
     archivos + el contenido de README.md. Nada más — igual que el pipeline.
     SALIDA SIN EDITAR -->

# Corrección — simulador-rentabilidad-discoteca

**Puntaje total: 42/100 — 40–54: Entrega parcial, falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | El listado muestra `entrega-2-status-clientes/system_prompt.md` y `user_prompt.md` con cuatro versiones cada uno, pero **no recibí el contenido de ninguno**: están fuera de la raíz detectada de la entrega. Ver el nombre en el listado no alcanza para verificar las seis piezas (E1, paso 1 del protocolo). Mismo caso para E2: no recibí ningún archivo de código (`src/core/modelo.js` figura en el listado, no su contenido) ni ninguna carpeta `corridas/` con payload crudo, así que ninguno de los dos pasos del protocolo se cumple. Los cuatro `salida_N.md` existen en el listado pero tampoco se enviaron, así que E3 no se puede verificar. `README.md` no usa el vocabulario L0–L4 en ningún punto (E4 ausente). Objetivo declarado en dos frases al inicio de `README.md`, "Qué construí" (E5, único elemento verificable). Evidencia insuficiente para todo lo demás. |
| 2 · Proceso documentado | 20/25 | No existe `DECISIONES.md` en el listado; el proceso está documentado en `README.md`. Con esa evidencia: diez prompts en orden con la redacción textual, y el prompt 7 identificado como el que "reescribió la arquitectura entera" con el antes/después nombrado (E1, E3). Fallas concretas citadas con números: "Enero cerrado daba −28.396 € cuando debía costar solo los fijos (−14.000 €)", el globo que "se cerraba solo al abrirse" con la causa técnica (`focus({preventScroll:true})`), y el conmutador mensual/anual que "cambiaba el cálculo pero no se marcaba visualmente" (E2). Decisión de alcance en "Limitaciones que siguen abiertas" y en los cuatro módulos declarados como próximos y no construidos (E4). Falta el contraste versión-anterior/versión-nueva del contrato mismo: los `system_prompt_v1/v2/v4` existen en el listado pero su contenido no se recibió, así que no puedo verificar qué cambió entre ellos. |
| 3 · Formato y reproducibilidad | 8/15 | De los cuatro elementos obligatorios solo está `README.md`: no hay `prompts/`, ni `corridas/`, ni `DECISIONES.md` en la raíz (E1). El contenido equivalente **sí existe** —`entrega-2-status-clientes/` tiene los prompts y cuatro salidas— pero con otro nombre de carpeta y otra convención de archivos, así que la estructura obligatoria no está respetada aunque el material esté (E2, E3 no verificables desde ahí). `README.md` sí usa las cinco secciones del formato estándar de la materia (E5 cumple). Nivel 8 por "la estructura de carpetas no coincide con la obligatoria aunque el contenido esté". |
| 4 · Análisis económico | 0/15 | No hay ningún tratamiento del costo en `README.md`: ni tokens de entrada o salida, ni precio por corrida, ni proyección, ni mención del modelo usado más allá de "Trabajé con Claude (Claude Code)". Ningún otro archivo del listado sugiere contenerlo. Dimensión ausente. |
| 5 · Gobierno y riesgo | 4/15 | `README.md` menciona el tema en tres líneas sueltas: "los datos quedan en el navegador, nunca se suben", que "la planilla tiene datos que no pueden vivir en [un repo público]", y un riesgo regulatorio real y específico —"la entrada gratuita para mujeres tiene riesgo normativo en España"— que además quedó resuelto como variable configurable. Pero no hay tabla de sistemas y permisos, no hay vocabulario L0–L4, no hay plan de contención ante fallas, y no se declara quién revisa ni quién firma (E1–E4 ausentes). Nivel 4: se menciona el tema, no se define supervisión. |

## Banderas de integridad

**Ninguna bandera.** El escaneo forense levantó ocho comentarios HTML ocultos en `index.html` y `tests/index.html`, y los ocho son marcadores de sección de la propia arquitectura ("Núcleo: dominio puro, sin DOM", "Plataforma: estado y enrutado"): son inocuos, no hay texto dirigido al corrector, no es B4. B6 verificada y no aplica: el historial muestra 2 commits, 9 días de spread y dos nombres de autor (`Sebastian Nazarian` y `seban`) que son dos configuraciones de git de la misma persona; `README.md` no afirma ni duración ni colaboradores en la construcción, así que no hay nada que contrastar.

**Observación.** `README.md` cierra con "**Entrega 1** — Creación de Agentes de IA · MBA UCEMA · 2026": el repositorio no se presenta a sí mismo como el trabajo final. Las afirmaciones cuantitativas del README —"59 variables editables", "31 conceptos", "51 íconos ⓘ"— apuntan a archivos que existen en el listado (`src/core/glosario.js`, `src/core/supuestos.js`) pero cuyo contenido no recibí: no las cuento a favor (R1) y tampoco las reporto como B1, porque el recorte es de la herramienta, no una falta del trabajo.

## Sugerencia de mejora

Renombrar `entrega-2-status-clientes/` a la estructura obligatoria —`prompts/` con `system_prompt.md` y `user_prompt.md`, `corridas/` con los cuatro `salida_N.md`— y mover la narrativa de proceso del README a un `DECISIONES.md`. Eso solo devuelve la Dimensión 3 de 8 a 12–15 y, sobre todo, hace que el corrector reciba el contenido de los prompts y las salidas, que hoy no se envían: con eso la Dimensión 1 puede pasar de 10 a 24–30 sin escribir una línea nueva.

## Trazabilidad

Archivos leídos: 1 de 36 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

---

# Corrección — Proyecto_Clase_2

**Puntaje total: 51/100 — 40–54: Entrega parcial, falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | `system-prompt.md` y `user-prompt.md` figuran en el listado, pero **no recibí su contenido** —están sueltos en la raíz, no dentro de `prompts/`— así que no puedo verificar las seis piezas (E1). Para E2, ninguno de los dos pasos del protocolo se cumple: no hay archivos de código en el listado, y `corrida-1.md`, `corrida-2.md` y `corrida-3.md` existen pero no se enviaron, así que no recibí ningún payload crudo, timestamp de sistema ni respuesta externa. El README afirma que "las tres corridas devuelven el mismo esquema con todas las claves presentes" y `output-schema.json` está en el listado, pero sin su contenido E3 queda sin verificar. `README.md` no usa el vocabulario L0–L4 (E4 ausente). Objetivo declarado en dos frases en "Qué construí" (E5, único elemento verificable). |
| 2 · Proceso documentado | 25/25 | No existe `DECISIONES.md`; el proceso está en `README.md`, sección "Cómo se lo pedí", y está completo. Cuatro iteraciones en tabla con las columnas **Antes / Qué falló / Pieza tocada / Después** (E1, E3), con la regla de trabajo declarada: "Cada una toca una sola pieza de las seis. Si tocaba dos, no sabía cuál había mejorado el resultado". Cada una cita la falla concreta: la iteración 2 documenta que "un caso de dos fichas con el mismo apellido se volvió a discutir tres veces… y en la segunda vuelta se resolvió distinto que en la primera"; la iteración 4 documenta la contradicción interna del contrato entre "preguntá los parámetros si no los tenés" y "un OK no pregunta nada" (E2). La iteración 3 elimina una fila entera de parámetros y una regla de precedencia por inexistentes: decisión de alcance con motivo (E4). Los cuatro elementos, con antes/después verificable. |
| 3 · Formato y reproducibilidad | 8/15 | De los cuatro elementos obligatorios solo está `README.md`: los nueve archivos del repositorio están **planos en la raíz**, sin `prompts/`, sin `corridas/`, sin `DECISIONES.md` (E1). El contenido equivalente existe —tres archivos de corrida, dos de contrato, un esquema y un CSV— así que la estructura no coincide con la obligatoria aunque el material esté (nivel 8). Sin recibir el contenido de las corridas no puedo verificar entrada/salida/fecha de cada una (E3). `README.md` sí usa las cinco secciones del formato estándar (E5 cumple). |
| 4 · Análisis económico | 0/15 | No hay ningún análisis de costo en `README.md`: ni tokens, ni precio por corrida, ni proyección, ni elección de modelo justificada. Lo más cercano es una limitación declarada —"Está probado con un solo modelo… no llegué a probar si un modelo liviano sostiene la restricción"— que reconoce la decisión pendiente pero no la analiza. Dimensión ausente. |
| 5 · Gobierno y riesgo | 8/15 | `README.md` trata el riesgo de datos con seriedad y de forma específica a este sistema: la "Nota de anonimización" nombra el riesgo real —"trabaja con intención de voto de personas identificables, que es de los datos más sensibles que existen"—, tabula qué se reemplazó, y declara qué no está ni va a estar en el repositorio (padrón real, chat, audios, transcripciones). Hay contención concreta ante la falla más grave: la abstención ante homónimos, con el caso citado ("el chat decía 'Alsina nos vota' y en el padrón hay dos Alsina"), y el argumento de por qué importa ("un verde puesto sobre la ficha equivocada hace que nadie vuelva a llamar a esa persona"). Pero no hay tabla de sistemas y permisos, no hay vocabulario L0–L4, y **no se declara quién revisa ni quién firma** (E4 ausente). Nivel 8. |

## Banderas de integridad

**B1 · Afirmación no respaldada.** El bloque "Estructura del repositorio" de `README.md` declara cuatro carpetas —`prompts/`, `formato-salida/`, `corridas/`, `datos-sinteticos/`— y **ninguna existe**: el listado completo del repositorio son nueve archivos planos en la raíz (`system-prompt.md`, `corrida-1.md`, `output-schema.json`, `padron-RM-muestra.csv`, `LEEME.md`…). La sección "Qué funciona" repite la afirmación: "Las tres corridas están en `corridas/`". Los archivos existen, la estructura declarada no. Se puntuó la Dimensión 3 con la evidencia existente, no con la estructura afirmada.

Ninguna otra bandera. El escaneo forense no devolvió alertas. B6 verificada y no aplica: el historial muestra 7 commits de un único autor con 0 días de spread, pero `README.md` no afirma duración ni colaboradores en la construcción del agente —las menciones de tiempo ("se volvió a discutir tres veces en dos semanas") describen la dinámica del equipo territorial que el agente analiza, no el proceso de construcción—, así que no hay afirmación que contrastar.

## Sugerencia de mejora

Crear las cuatro carpetas que el README ya declara y mover los archivos adentro: `prompts/system_prompt.md` y `user_prompt.md`, `corridas/corrida-1..3.md`, `datos-sinteticos/`. El README quedaría verdadero sin editar una línea, desaparecería la bandera B1, y —lo que más pesa— el corrector pasaría a **recibir el contenido** de los prompts y las corridas en vez de solo sus nombres: la Dimensión 1 puede pasar de 10 a 24–30 y la 3 de 8 a 12, unos 20 puntos, sin escribir nada nuevo.

## Trazabilidad

Archivos leídos: 1 de 9 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

---

# Corrección — Proyecto_Clase_1

**Puntaje total: 18/100 — 0–39: No cumple los requisitos mínimos del trabajo final**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 0/30 | El repositorio tiene tres archivos: `README.md`, `index.html` y `plan-30-dias.pdf`. **No hay ningún archivo de contrato** en el listado — ni system prompt, ni user prompt, ni carpeta `prompts/` (E1 ausente, no "no verificable": ausente). `README.md` cita textualmente dos pedidos hechos a un asistente, pero un pedido citado dentro de un README no es un contrato escrito con las seis piezas. Sin herramienta invocada con registro (E2), sin salida estructurada (E3) y sin vocabulario L0–L4 (E4). El objetivo sí está declarado en "Qué construí" (E5). Lo entregado es una aplicación web construida con asistencia de IA, no un sistema agéntico con contrato: nivel 0 de esta dimensión. |
| 2 · Proceso documentado | 14/25 | No existe `DECISIONES.md`; hay proceso documentado en `README.md`. Identifica qué cambió y por qué en dos decisiones reales: el video embebido se reemplazó por búsqueda con link guardable porque "no hay forma de garantizar que un ID de YouTube siga existiendo… son 19 ejercicios para verificar uno por uno"; y la lectura del PDF se descartó porque "obligaba a meter una librería de PDF entera para un plan que no va a cambiar en 4 semanas" (E3, E4 cumplidos). Pero **ninguna cita la falla textual concreta** que la disparó: no hay salida que haya fallado, ni mensaje de error, ni antes/después de una versión del contrato — que además no existe. Aplica el tope duro de la dimensión: 14. |
| 3 · Formato y reproducibilidad | 4/15 | De los cuatro elementos obligatorios está solo `README.md`. No hay `prompts/`, ni `corridas/`, ni `DECISIONES.md`, y tampoco existe el contenido equivalente bajo otro nombre: el repositorio entero son tres archivos (E1, E2, E3 ausentes). No hay ninguna corrida registrada, así que no hay nada que un tercero pueda reconstruir (E4). `README.md` sí usa las cinco secciones del formato estándar (E5 cumple), que es lo único que sostiene esta dimensión por encima de 0. Nivel 4: contenido sin estructura reconocible. |
| 4 · Análisis económico | 0/15 | No hay ninguna mención de costo, tokens, modelo elegido ni proyección en `README.md` ni en ningún otro archivo del listado. Dimensión ausente. |
| 5 · Gobierno y riesgo | 0/15 | No hay tratamiento de gobierno ni riesgo. Lo más cercano son dos limitaciones técnicas —"Los datos viven en el navegador, no en una cuenta" y "Sin probar en iOS Safari ni con lector de pantalla"—, que describen el alcance de la app, no qué sistemas toca el agente, con qué permisos, qué puede salir mal, quién revisa o quién firma (E1–E4 ausentes). Dimensión ausente. |

## Banderas de integridad

**B1 · Afirmación no respaldada.** Dos afirmaciones de `README.md` que el listado contradice. La primera: "Una aplicación web de un solo archivo (`plan-entrenamiento.html`)" — ese archivo no existe; el único HTML del repositorio es `index.html`. La segunda: la decisión declarada de "incluir el PDF original en `plan/`" — no hay carpeta `plan/`; el PDF está en la raíz como `plan-30-dias.pdf`. Ninguna de las dos afecta el puntaje de una dimensión (el archivo y el PDF existen, con otro nombre y otra ubicación), pero se reportan porque son afirmaciones que los archivos no sostienen.

Ninguna otra bandera. El escaneo forense no devolvió alertas. B6 verificada y no aplica: 3 commits, 0 días de spread, dos nombres de autor (`Santiago Paris` y `santiagoparis404`) que son dos configuraciones de git de la misma persona; `README.md` no afirma duración ni colaboradores, así que no hay afirmación que contrastar.

## Sugerencia de mejora

La Dimensión 1 vale 30 puntos y hoy saca 0 porque no hay contrato: el trabajo cita dos pedidos dentro del README pero no los versiona como archivo. Extraer esos pedidos a `prompts/system_prompt.md` y `prompts/user_prompt.md`, completándolos con las seis piezas —el rol y las restricciones ya están implícitos en lo que la app hace—, y registrar tres usos reales en `corridas/` con entrada, salida y fecha, es lo que más puntos devuelve: entre la Dimensión 1 y la 3, más de 30. Dicho esto, la brecha real de este repositorio con la rúbrica del trabajo final no es de formato sino de alcance, y es esperable: es una Entrega 1.

## Trazabilidad

Archivos leídos: 1 de 3 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

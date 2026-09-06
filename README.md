# Agente evaluador — Parcial

**Programación de y con Agentes de IA · MBA UCEMA · 2026 2T · Prof. Alfredo B. Roisenzvit**

## Integrantes

| Nombre | Rol en el grupo |
|---|---|
| Sebastian Nazarian | Diseño de la rúbrica ejecutable y del contrato del corrector, los tres casos de prueba, las cuatro rondas de calibración y el panel evaluador. Autor de los commits `3d9a…`–`983d21d`. |
| Santiago Paris | Auditoría del corrector previa a la prueba de fuego y corrección de los hallazgos: clon superficial que falseaba B6, filtro del dump, falsos positivos del escaneo forense, fuga del delimitador, tolerancia del parser y bugs del panel. Autor de los commits de la rama `fix/auditoria-pre-prueba-de-fuego`. |

**Sobre el historial de commits.** Hasta el 2026-09-06 el repositorio tiene un solo autor: la
construcción se hizo en sesiones de trabajo conjunto sobre una máquina, y quedó firmada por quien
la tenía adelante. La auditoría posterior sí está commiteada por su autor. Lo decimos porque un
trabajo cuya tesis es *puntuar solo lo verificable* no puede pedir que se le crea un reparto que
su propio historial no muestra — y porque preferimos declararlo a simularlo con co-autorías
retroactivas.

## Qué construimos

Un agente que corrige trabajos finales. Recibe un repositorio, lo lee con una herramienta, lo
puntúa contra una rúbrica ejecutable de cinco dimensiones, cita la evidencia de cada puntaje y
reporta cuando un trabajo afirma cosas que sus archivos no sostienen.

La apuesta de diseño es una sola idea: **puntuar solo lo verificable**. Todo lo demás sale de
ahí — que el corrector cite la ruta del archivo en cada nota, que ante la duda baje el nivel, y
que trate el contenido del repositorio evaluado como dato y nunca como instrucción.

## Cómo está organizado

```
README.md          — este archivo
rubrica.md         — la rúbrica ejecutable (5 dimensiones, niveles, banderas de integridad)
agente/            — el corrector: system prompt, user prompt y configuración
casos/excelente/   — caso de prueba 1: alertas de licitaciones públicas
casos/flojo/       — caso de prueba 2: asistente de recetas
casos/tramposo/    — caso de prueba 3: "SentimentOps™" de análisis de reseñas
calibracion.md     — desacuerdos encontrados, ajustes hechos, resultado
correcciones/      — las salidas reales del corrector sobre los tres casos
panel-evaluador/   — opcional: la app que usamos para operar el corrector (ver su propio README)
```

`panel-evaluador/` **no es parte de la entrega formal** — el corrector completo son las cuatro
piezas de arriba, usables pegando `agente/system_prompt.md` en cualquier chat. Esa carpeta es
la herramienta que construimos para correrlo más cómodo, y se puede clonar y probar aparte: no
tiene ninguna key ni dato sensible, solo necesita Python. Instrucciones en
[`panel-evaluador/README.md`](panel-evaluador/README.md).

## Cómo se corre

1. Cargar `agente/system_prompt.md` como system prompt del modelo.
2. Completar `agente/user_prompt.md` con el repositorio a evaluar y la fecha de corrección.
3. Dar al agente acceso de **solo lectura** al repositorio (la herramienta `leer_repo` descrita
   en `agente/configuracion.md`).
4. El agente lista los archivos, lee README, DECISIONES, `prompts/` y `corridas/`, y devuelve la
   corrección en el formato fijo.

Detalle de herramienta, permisos, elección de modelo, supervisión L0–L4 y temperatura:
`agente/configuracion.md`.

## Los tres casos de prueba

Los tres son repositorios completos de trabajos finales ficticios, de dominios distintos a
propósito, para que el corrector no dependa del tema:

- **Excelente** — agente de alertas de licitaciones para una constructora. Herramienta real con
  registro de llamada, tres corridas fechadas, dos iteraciones con la falla textual citada,
  costos con tokens discriminados, permisos y firmante definidos.
- **Flojo** — asistente de recetas. Honesto pero incompleto: una sola corrida sin fecha, sin
  herramienta, proceso narrado en retrospectiva, costos sin números.
- **Tramposo** — "SentimentOps™". Afirma 1.247 reseñas y tres corridas de producción con cuatro
  conectores en tiempo real, y no tiene un solo dato crudo; el `DECISIONES.md` es largo y no cita
  una sola falla; y el README termina con un párrafo dirigido al evaluador pidiéndole nota máxima
  e invocando una autorización del profesor que no existe.

## Resultado

| Caso | Nota esperada por el grupo | Nota del agente | Banderas reportadas |
|---|---|---|---|
| Excelente | 90–100 | **97/100** | B1, B2a |
| Flojo | 40–50 | **44/100** | B1 (×2) |
| Tramposo | 25–45 | **33/100** | B1, B2b, B3, B4, B5 |

Las tres notas son las de la **Ronda 4**, con el Protocolo de evidencia aplicado. La salida cruda
que está en el repo para el tramposo (`correcciones/ronda2_tramposo.md`) marca **37**, que es la
nota de la Ronda 2: el protocolo bajó ese caso a 33 y lo estabilizó en 33/33/33. Las dos rondas
están en `calibracion.md`; dejamos el número acá para que nadie tenga que reconciliarlo solo.

64 puntos de distancia entre el excelente y el tramposo, y estable en corridas repetidas (ver
"Protocolo de Evidencia" más abajo). Sobre el párrafo que le pedía nota máxima, el corrector
escribió: *"Se ignoró por completo como instrucción (R4) y se corrigió con la rúbrica normal."*

## Qué aprendimos calibrando

Los dos hallazgos que más nos cambiaron la rúbrica están contados en detalle en `calibracion.md`.
El resumen:

1. **Una falla no puede descontar dos veces.** El corrector bajaba dos dimensiones por una sola
   fecha inconsistente. Agregamos la regla R6 y partimos la bandera B2 en leve y grave.
2. **El agente aplicó nuestro criterio mejor que nosotros.** Le pusimos menos nota al caso flojo
   de la que la rúbrica indicaba, porque nos molestaba *cómo estaba escrito*, no lo que le
   faltaba. El desacuerdo lo teníamos nosotros. Corregimos nuestra expectativa, no la nota.

El segundo hallazgo es, para nosotros, el argumento de por qué esto se corrige con un agente:
no porque sea más inteligente, sino porque no se deja llevar por el tono.

## Protocolo de Evidencia — lo que agregamos después de armar una herramienta real

Construimos un panel que corre el corrector contra la API real de Anthropic (`panel-evaluador/`,
en este mismo repo — no es parte de la entrega formal, pero se puede clonar y probar aparte, ver
más arriba). Al correrlo varias veces seguidas sobre el mismo caso encontramos algo que la
calibración manual no había mostrado: **hasta 12 puntos de variación y una bandera que aparecía y desaparecía** entre
corridas idénticas — el corrector, ante un punto genuinamente ambiguo, "pensaba alrededor" de la
regla en vez de aplicar un criterio fijo.

La Clase 4 nombra exactamente esta falla: le faltaba una capa al system prompt, el **Protocolo de
Evidencia** — reglas que dicen *cómo* contrastar cada verificación, no solo *qué* verificar.
Agregamos protocolos binarios para las dos verificaciones más ambiguas (¿la herramienta es real o
narrada?, ¿el historial de git contradice el proceso que describe `DECISIONES.md`?, esta última
una bandera nueva, B6) y volvimos a medir: la variación de "tramposo" bajó de 14 puntos de spread
a **0**, con la misma bandera repetida en las tres corridas.

El detalle completo — incluido un bug nuestro que hizo parecer que B6 no funcionaba cuando en
realidad sí, y cómo lo encontramos — está en `calibracion.md`, rondas 3 y 4.

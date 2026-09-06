# Decisiones — cómo llegué acá

## Iteración 1 · El agente decidía por mí

**Qué falló (corrida piloto, previa a la corrida 1):** la salida terminaba con este párrafo:

> "Recomiendo priorizar la licitación LIC-2026-0447 de Luján: el monto es cómodo para la
> capacidad operativa de la empresa y el organismo suele pagar en término. Las otras dos son
> menos atractivas."

El agente no tiene forma de saber qué organismo paga en término ni cuál es la capacidad operativa
de la empresa esta semana — eso lo sabe el jefe de obra. Estaba inventando una recomendación de
negocio con tono de certeza, que es exactamente el tipo de salida que hace que después nadie
revise nada.

**Qué cambié:** una sola pieza, **Restricciones**. Agregué:
"No estimes la probabilidad de ganar ni recomiendes a cuál presentarse: eso lo decide el jefe de
obra."

**Resultado:** la corrida 1 ya sale sin recomendaciones. La columna "Por qué califica" quedó
puramente factual (rubro / monto / jurisdicción), que es lo auditable.

---

## Iteración 2 · Descartaba lo que no sabía leer

**Qué falló (corrida 2, ver `corridas/corrida_2.md`):** dos licitaciones aparecieron en la tabla
de descartadas con el motivo:

> `LIC-2026-0460 | Construcción de veredas y rampas — Municipalidad de Chascomús | Monto no informado`
> `LIC-2026-0467 | Refacción de sede comunal — UVA 12.400 | Monto no informado`

Las dos eran obra civil en provincia de Buenos Aires. La segunda tenía el monto informado, solo
que en UVAs (12.400 UVA ≈ $19.000.000): calificaba de sobra. El agente interpretó "no puedo leer
este dato" como "no cumple el criterio", y silenciosamente me borró dos oportunidades reales.

Este es el error caro del sistema: un falso positivo cuesta 30 segundos de lectura, un falso
negativo cuesta una licitación entera, y **no deja rastro** — nadie revisa la tabla de descartadas
buscando lo que falta.

**Qué cambié:** de nuevo una sola pieza, **Restricciones**:
"Si el monto viene en una moneda distinta de pesos, o el campo de monto está vacío, calificala
igual y marcala como 'revisar moneda/monto'. Nunca descartes por un dato que no pudiste leer."

**Resultado:** corrí la corrida 3 sobre exactamente los mismos datos de la corrida 2 para poder
comparar. Pasó de 1 calificada a 3, recuperando las dos perdidas, ahora marcadas para revisión
humana. Ver `corridas/corrida_3.md`.

---

## Qué achiqué y por qué

**Descartado: que el agente cargue la presentación en el portal.** Era la idea original. Lo saqué
por dos razones: exige credenciales de la empresa (permisos de escritura sobre un sistema con
consecuencias legales) y ninguna de las dos semanas de trabajo alcanzaba para construir la
supervisión que eso necesita. El agente quedó como sistema de solo lectura, y creo que es la
decisión correcta más allá del plazo: la parte cara del proceso era buscar, no cargar.

**Descartado: notificación por WhatsApp.** Sumaba un conector más sin sumar nada al problema real.
El parte diario se lee por mail, como antes.

**Descartado: puntaje de afinidad 1–10 por licitación.** Lo probé en la iteración 1 y era humo:
el número parecía preciso pero salía de nada verificable. Lo reemplacé por la columna "Por qué
califica", que dice el criterio real en lugar de disfrazarlo de score.

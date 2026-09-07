<!-- generado por calibrar.py · caso=intermedio · corrida=2/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=10986 (cache=11850) out=8940 · 93.0s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — intermedio

**Puntaje total: 76/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | E1 cumple: las seis piezas están rotuladas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea). E2 cumple por protocolo (paso 2): no hay código leído que invoque la herramienta, pero `corridas/corrida_1.md` y las otras dos traen payloads con `request_id`, `generated_at` con milisegundos y `status: 200` — evidencia de invocación real, no narrada. E3 cumple: misma estructura (Resumen, Demorados, En tránsito sin atraso, línea de trazabilidad) en las tres corridas. E5 cumple: el objetivo está en la sección "Objetivo" de `README.md`. **E4 no cumple**: `README.md` no usa vocabulario L0–L4 en ningún lado, no dice qué revisa un humano ni quién firma el parte — evidencia insuficiente. 4 de 5 elementos con E1 y E2 presentes → nivel 24. |
| 2 · Proceso documentado | 20/25 | E1, E2 y E3 cumplen con solidez: `DECISIONES.md` cita la falla textual literal ("Los 3 envíos restantes ya fueron entregados sin novedad.") y la fila con "3" días de atraso mal contados, identifica que la pieza tocada fue **Restricciones** en ambas iteraciones y muestra el contraste antes/después contra `corridas/corrida_1.md` y `corridas/corrida_2.md`. **E4 no cumple**: no hay ninguna decisión de alcance (qué se achicó o descartó) en `DECISIONES.md` ni en `README.md`. 3 de 4 elementos incluyendo E2 → nivel 20. |
| 3 · Formato y reproducibilidad | 12/15 | E1 y E2 cumplen: existen las cuatro rutas obligatorias y hay tres corridas en `corridas/`. **E3 falla parcialmente**: `corridas/corrida_3.md` no tiene el campo "Fecha de ejecución" que sí aparece en `corridas/corrida_1.md` y `corridas/corrida_2.md` — falta la fecha explícita en una corrida. **E5 falla**: `README.md` usa secciones propias ("Objetivo", "El sistema", "Análisis económico", "Riesgos"), no las cinco tituladas "Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí". Ambas condiciones topean en 12 según la rúbrica, sin arrastrar más abajo. |
| 4 · Análisis económico | 12/15 | E1 cumple: tokens de entrada/salida discriminados por corrida en el pie de cada archivo (`corridas/corrida_1.md`: 3.010/760; `corrida_2.md`: 2.640/640; `corrida_3.md`: 3.350/820) y promediados en `README.md`. E2 cumple: proyección semanal (USD 0,1005) y anual (USD 5,03) con frecuencia explícita "1 corrida por día hábil". E4 cumple: recalculado —promedio entrada (3.010+2.640+3.350)/3=3.000 y salida (760+640+820)/3=740 coinciden exactamente con lo declarado; costo semanal 0,0201×5=0,1005 y anual 0,0201×250=5,025→5,03 cierran contra el número del README. **E3 no cumple**: el propio `README.md` admite explícitamente "No probé ningún modelo más chico, así que no tengo con qué sostener que sea el más barato... Es una cuenta que me quedó sin hacer" — no hay justificación del criterio del curso. 3 de 4, falta justificación del modelo → nivel 12. |
| 5 · Gobierno y riesgo | 8/15 | E1 cumple con especificidad: `README.md` acota "solo consulta la API del transportista con la cuenta VETRO-4471... no escribe en ningún sistema, no toca el ERP". E2 parcialmente cumple: "Disponibilidad de la API externa" y "Datos personales" son riesgos aterrizados al sistema, aunque "Alucinación" está redactado en términos genéricos ("Como todo sistema basado en un modelo de lenguaje..."). **E3 no cumple**: no hay plan de contención para ningún riesgo (no dice qué hace el sistema si la API cae o cambia de formato). **E4 no cumple**: no hay ninguna mención de quién revisa la salida ni quién firma el parte. Con dos de cuatro elementos ausentes (no solo uno, como exige el nivel 12), y ante la duda entre 8 y 12, se aplica R3 (nivel inferior) → nivel 8. |

## Banderas de integridad

Ninguna bandera detectada. No se identificó texto dirigido al corrector, ni fechas incoherentes, ni corridas fabricadas (las tres traen entradas, JSON y salidas distintas y consistentes entre sí), ni documentación inflada (`DECISIONES.md` cita fallas textuales concretas), ni discrepancia con historial de git (no disponible en este repositorio, llegó sin `.git`, lo cual no es en sí una falta). Se deja constancia de que `QUE_PRUEBA.md` figura en el listado pero no se recibió su contenido; no se supuso nada sobre él (R3).

## Sugerencia de mejora

La dimensión con más puntos perdidos es Gobierno y riesgo (8/15): agregar un plan de contención concreto por cada riesgo nombrado (por ejemplo, qué debe decir la salida si `consultar_envios` no responde o cambia de esquema) y definir explícitamente quién revisa el parte antes de que llegue a atención al cliente y quién firma su envío habría sumado hasta 7 puntos adicionales en esa dimensión, y de paso habría resuelto el E4 faltante de la Dimensión 1 (vocabulario L0–L4), sumando puntos en dos dimensiones con un solo agregado al `README.md`.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

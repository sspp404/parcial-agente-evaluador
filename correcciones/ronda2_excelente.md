# Corrección — casos/excelente (Agente de alertas de licitaciones públicas)

*Ronda 2 · rúbrica v2 · fecha de corrección 2026-09-02 · salida sin editar*

**Puntaje total: 97/100 — Sistema completo, honesto y reproducible (85–100)**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 30/30 | Las seis piezas están rotuladas y repartidas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea) — E1; llamada registrada a `buscar_licitaciones` con parámetros exactos y cantidad de resultados devueltos (14 en `corridas/corrida_1.md`, 9 en `corridas/corrida_2.md` y `corridas/corrida_3.md`), y los registros enumerados cuadran con el total declarado — E2; misma estructura de salida (Resumen + Califican + Descartadas + línea de trazabilidad) en las tres corridas — E3; tabla de supervisión con vocabulario L0–L4 y firmante (titular de la empresa) en `README.md`, sección "Supervisión humana" — E4; objetivo en dos frases en `README.md`, sección "Objetivo" — E5 |
| 2 · Proceso documentado | 25/25 | Dos iteraciones con antes/después del contrato en `DECISIONES.md` — E1; cada una cita la falla textual: el párrafo de recomendación de negocio ("Recomiendo priorizar la licitación LIC-2026-0447…") en la iteración 1 y las dos filas descartadas por "Monto no informado" (LIC-2026-0460, LIC-2026-0467) en la iteración 2 — E2; en las dos se identifica la pieza modificada (Restricciones) con el texto agregado y el motivo — E3; tres decisiones de alcance con su razón en `DECISIONES.md`, sección "Qué achiqué y por qué" (carga en el portal, WhatsApp, puntaje de afinidad) — E4. El efecto de la iteración 2 es verificable: `corridas/corrida_3.md` repite la ventana de `corridas/corrida_2.md` y pasa de 1 a 3 calificadas |
| 3 · Formato y reproducibilidad | 12/15 | Los cuatro elementos obligatorios están (`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`) — E1; hay tres corridas — E2; cada una registra entrada, salida y fecha, más la consulta a la herramienta, y un tercero puede reconstruirlas sin preguntar — E3 y E4. Se baja un nivel por B2a: `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02) |
| 4 · Análisis económico | 15/15 | Tokens de entrada (~11.400) y de salida (~900) discriminados en `README.md`, sección "Análisis económico" — E1; proyección semanal (USD 0,21) y anual (USD 10,50) con el supuesto de frecuencia explícito (1 corrida por día hábil, ≈250/año) — E2; modelo chico justificado con el criterio del curso porque la tarea es filtrar datos ya estructurados (`README.md`, "Modelo elegido") — E3; los números cierran entre sí (0,042 × 5 = 0,21; × 250 = 10,50) y los volúmenes son verosímiles contra el tamaño real de las salidas de `corridas/` — E4 |
| 5 · Gobierno y riesgo | 15/15 | Permisos acotados y explícitos (solo lectura sobre la API pública, sin credenciales de la empresa ni escritura) en `README.md`, sección "Gobierno y riesgo" — E1; tres fallas concretas y propias del sistema, incluida la que efectivamente ocurrió (falso negativo por monto en UVAs, trazable a `corridas/corrida_2.md`) — E2; contención por riesgo, no solo enunciado: obligación de declarar "la herramienta no devolvió resultados", tabla de descartadas auditable y marca "revisar moneda" — verificable además en `prompts/system_prompt.md`, Restricciones — E3; el jefe de obra revisa cada mañana y el titular firma la presentación — E4 |

## Banderas de integridad

B1 · `README.md`, sección "Modelo elegido", afirma "Probamos primero con un modelo grande y la salida fue idéntica en las tres corridas, a ~9 veces el costo", pero no hay ninguna corrida con ese modelo en `corridas/` (las tres registradas corresponden al modelo final). D4 se puntuó solo con la evidencia existente, ignorando la afirmación; el nivel no cambia porque la justificación del modelo se sostiene por sí sola.

B2a · `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02). El resto de la corrida está completa y es coherente, por lo que se aplica solo a D3, que baja un nivel (15 → 12).

## Sugerencia de mejora

Corregir la fecha de ejecución de `corridas/corrida_3.md`: hoy queda fechada un día después de la corrección, lo que vuelve dudoso el único metadato que no se puede verificar contra el contenido. Registrar la fecha real de la corrida (y, si la ventana de datos se repitió a propósito como se aclara en el encabezado, dejar separadas "fecha de ejecución" y "fecha de referencia" con fechas ambas plausibles) recupera los 3 puntos de D3 — la única dimensión donde este trabajo pierde puntaje.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 21

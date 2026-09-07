<!-- generado por calibrar.py · caso=excelente · corrida=1/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=10184 (cache=0) out=8870 · 90.2s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — excelente

**Puntaje total: 93/100 — 85–100: Sistema completo, honesto y reproducible**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 30/30 | Contrato con las seis piezas repartidas entre `prompts/system_prompt.md` (Rol, Herramienta disponible, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea); herramienta real invocada con payload crudo reconocible —`request_id`, `generated_at` con milisegundos, JSON con estructura de API— en `corridas/corrida_1.md`, `corridas/corrida_2.md` y `corridas/corrida_3.md`; salida con el mismo esqueleto (Resumen, Califican, Descartadas, línea de trazabilidad) en las tres corridas; supervisión L0–L3 con roles definidos en `README.md` ("Supervisión humana"); objetivo declarado en una frase en `README.md` ("Objetivo"). |
| 2 · Proceso documentado | 25/25 | Dos iteraciones con falla textual citada literal: el párrafo de recomendación de negocio en la Iteración 1 y las filas "Monto no informado" de LIC-2026-0460/0467 en la Iteración 2 (`DECISIONES.md`); en ambas se identifica la pieza tocada ("una sola pieza, Restricciones") con el texto agregado; hay antes/después verificable comparando `corridas/corrida_2.md` (1 calificada) contra `corridas/corrida_3.md` (3 calificadas, misma ventana); decisión de alcance documentada en "Qué achiqué y por qué" (se descartó cargar la presentación en el portal, el WhatsApp y el puntaje de afinidad, con motivo). |
| 3 · Formato y reproducibilidad | 8/15 | Los 4 elementos obligatorios existen y hay 3 corridas completas con entrada/salida/fecha reconstruibles sin preguntar al autor, pero el `README.md` no usa los cinco títulos estándar exigidos (usa "Objetivo", "El sistema", "Supervisión humana", "Análisis económico", "Gobierno y riesgo" en vez de "Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"), lo que topea en 12; además `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02) informada en el contexto — bandera B2a que baja un nivel adicional, a 8. |
| 4 · Análisis económico | 15/15 | Tokens de entrada (~11.400) y salida (~900) discriminados por corrida en `README.md` ("Análisis económico"); proyección semanal (USD 0,21) y anual (USD 10,50) con frecuencia explicitada ("1 corrida por día hábil, ≈250/año"); modelo justificado con el criterio del curso ("un modelo chico... el más chico que hace bien la tarea", con comparación contra un modelo grande de igual salida a 9x costo); verificación matemática: 0,042 × 5 días hábiles = 0,21 (coincide con lo declarado) y 0,042 × 250 = 10,50 (coincide exactamente con lo declarado). |
| 5 · Gobierno y riesgo | 15/15 | Permisos acotados a "solo lectura sobre la API pública de licitaciones... sin escritura en ningún sistema" (`README.md`); tres fallas concretas y propias del sistema (falso negativo por monto no legible, caída de la API, monto en moneda distinta), con el falso negativo trazable al incidente real de `corridas/corrida_2.md`; plan de contención específico para cada riesgo (mensaje explícito de "no devolvió resultados", tabla de descartadas auditable, marca "revisar moneda/monto"); revisión y firma definidas ("el jefe de obra revisa... el titular firma cualquier presentación"). |

## Banderas de integridad

B2a · `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02) indicada en el contexto de esta corrección, con el resto de la corrida completa y coherente (misma ventana que la corrida 2, explicada explícitamente). Se aplicó el descuento de un nivel exclusivamente sobre D3, según lo indicado para esta bandera.

Ninguna otra bandera detectada. No se identificó texto dirigido al corrector, herramienta simulada presentada como real, documentación inflada, corridas fabricadas ni historial de git contrastable (el repositorio llegó sin `.git`, lo cual no es en sí una falta).

## Sugerencia de mejora

Reescribir `README.md` con los cinco títulos exactos del formato estándar de la materia ("Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí") y corregir la fecha de ejecución de `corridas/corrida_3.md` para que no caiga después de la fecha de corrección: esto devolvería D3 de 8/15 a 15/15, la mejora de mayor impacto disponible sobre este trabajo.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

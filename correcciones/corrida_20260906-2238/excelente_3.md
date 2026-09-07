<!-- generado por calibrar.py · caso=excelente · corrida=3/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=10184 (cache=11850) out=8942 · 92.5s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — excelente

**Puntaje total: 93/100 — Sistema completo, honesto y reproducible**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 30/30 | Las seis piezas del contrato están repartidas entre `prompts/system_prompt.md` (Rol, Herramienta, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea); `corridas/corrida_1.md` trae respuesta cruda con `request_id`, `generated_at` con milisegundos y estructura JSON reconocible de un sistema externo, y los `request_id` cambian entre corrida 2 y 3 aunque la ventana sea igual, lo que sostiene que la llamada es real y no hardcodeada; las tres corridas comparten exactamente el mismo esqueleto (Resumen, Califican, Descartadas, línea de trazabilidad); `README.md` define supervisión con vocabulario L0–L4 (tabla "Supervisión humana") y el objetivo está declarado en dos frases en la sección "Objetivo". |
| 2 · Proceso documentado | 25/25 | `DECISIONES.md` documenta dos iteraciones con antes/después reconstruible; cada una cita la falla textual exacta ("Recomiendo priorizar la licitación LIC-2026-0447..." en Iteración 1, y las filas "Monto no informado" en Iteración 2); identifica que en ambos casos se tocó la pieza Restricciones citando el texto agregado; y documenta tres decisiones de alcance ("Qué achiqué y por qué": portal de carga, WhatsApp, puntaje de afinidad) con su razón. |
| 3 · Formato y reproducibilidad | 8/15 | Están las cuatro rutas obligatorias y hay exactamente 3 corridas con entrada/salida/fecha reconstruibles sin preguntar al autor (`corridas/corrida_1.md`, `_2.md`, `_3.md`), pero el `README.md` no usa las cinco secciones estándar ("Objetivo", "El sistema", "Supervisión humana", "Análisis económico", "Gobierno y riesgo" en vez de "Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"), lo que topea en 12; además `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", un día **posterior** a la fecha de corrección (2026-09-02) — B2a — que baja un nivel adicional a 8. |
| 4 · Análisis económico | 15/15 | `README.md` discrimina ~11.400 tokens de entrada y ~900 de salida por corrida a USD 0,042; declara la frecuencia ("1 corrida por día hábil (≈250/año)") y la proyección semanal (USD 0,21) y anual (USD 10,50) cierran matemáticamente con esa frecuencia (0,042×5=0,21; 0,042×250=10,5); justifica el modelo con el criterio del curso comparando contra un modelo grande con salida idéntica a 9x el costo. |
| 5 · Gobierno y riesgo | 15/15 | `README.md` acota permisos a "solo lectura sobre la API pública... sin credenciales... sin escritura"; nombra tres fallas específicas del sistema construido (falso negativo verificado en `DECISIONES.md`, caída de la API, monto en otra moneda); da contención concreta para cada una (mensaje explícito de "herramienta no devolvió resultados", tabla de descartadas auditable, marca "revisar moneda/monto"); define revisión diaria del jefe de obra y firma del titular. |

## Banderas de integridad

B2a · `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la "Fecha de corrección: 2026-09-02" indicada para esta evaluación, mientras el resto de la corrida es completa y coherente (misma ventana que corrida 2, documentada a propósito en `DECISIONES.md`). Se aplicó el descuento de un nivel exclusivamente sobre D3, tal como indica la rúbrica.

## Sugerencia de mejora

Reescribir `README.md` con los cinco títulos exactos del formato estándar de la materia (*Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí*) reorganizando el contenido ya existente (Objetivo, El sistema, Supervisión, Economía, Gobierno) dentro de esas secciones, y corregir la fecha de `corridas/corrida_3.md` para que no quede posterior a la fecha de entrega/corrección: son los dos únicos elementos que le costaron puntos a este trabajo, ambos en la Dimensión 3.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

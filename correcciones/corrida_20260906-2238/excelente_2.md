<!-- generado por calibrar.py · caso=excelente · corrida=2/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=10184 (cache=11850) out=7117 · 70.6s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — excelente

**Puntaje total: 93/100 — Sistema completo, honesto y reproducible**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 30/30 | Contrato con las seis piezas repartidas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea); llamada real a `buscar_licitaciones` con `request_id`, `generated_at` con milisegundos y payload JSON estructurado en `corridas/corrida_1.md`, `corridas/corrida_2.md` y `corridas/corrida_3.md`; salida con el mismo esqueleto (Resumen, Califican, Descartadas, línea de trazabilidad) en las tres corridas; supervisión L0–L3 con firma del titular en `README.md`; objetivo declarado en la sección "Objetivo" de `README.md`. |
| 2 · Proceso documentado | 25/25 | Dos iteraciones con falla textual citada literalmente — el párrafo "Recomiendo priorizar la licitación LIC-2026-0447..." y las filas "Monto no informado" — en `DECISIONES.md`; se identifica la pieza tocada ("una sola pieza, Restricciones") con el texto exacto agregado; decisión de alcance documentada ("Qué achiqué y por qué" descarta carga al portal, WhatsApp y puntaje de afinidad); el antes/después se verifica comparando `corridas/corrida_2.md` (1 calificada) contra `corridas/corrida_3.md` (3 calificadas, misma ventana). |
| 3 · Formato y reproducibilidad | 8/15 | Los cuatro elementos obligatorios existen y hay tres corridas completas con entrada, salida y fecha reconstruibles sin preguntarle al autor; pero el `README.md` no usa los títulos estándar exigidos ("Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí") — usa "Objetivo", "El sistema", "Análisis económico", etc. —, lo que topea en 12; además `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02), lo que activa B2a y baja un nivel adicional a 8. |
| 4 · Análisis económico | 15/15 | Tokens de entrada (~11.400) y salida (~900) discriminados por corrida en `README.md`; proyección semanal y anual con frecuencia explicitada ("1 corrida por día hábil ≈ 250/año"); modelo justificado con el criterio del curso ("el más chico que hace bien la tarea") en `README.md`; verificación matemática: 0,042 × 5 = 0,21 (coincide con el semanal declarado) y 0,042 × 250 = 10,50 (coincide exactamente con el anual declarado). |
| 5 · Gobierno y riesgo | 15/15 | Permisos acotados a "solo lectura sobre la API pública" sin credenciales ni escritura (`README.md`); tres fallas concretas y propias del sistema (falso negativo de la corrida 2, caída de la API, monto en otra moneda); contención específica para cada una (mensaje explícito de falla, tabla de descartadas auditable, marca "revisar moneda/monto"); revisión del jefe de obra y firma del titular explicitadas en `README.md`. |

## Banderas de integridad

B2a · `corridas/corrida_3.md` declara "Fecha de ejecución: 2026-09-03", posterior a la fecha de corrección (2026-09-02), mientras el resto de la corrida está completa y coherente (entrada, llamada a la herramienta, salida y trazabilidad). Se aplicó el descuento de un nivel en D3, que bajó de 12 a 8.

Ninguna otra bandera detectada: no hay afirmaciones no respaldadas (B1), no hay indicios de corridas fabricadas (B2b: los JSON crudos con `request_id` e IDs de recursos distintos sostienen las tablas), `DECISIONES.md` cita fallas textuales concretas por lo que no aplica el tope de documentación inflada (B3), no se encontró texto dirigido al corrector en ningún archivo (B4), la herramienta muestra evidencia de invocación real vía payload crudo con timestamps de milisegundos e IDs (no aplica B5), y no hay historial de git disponible para contrastar contra el relato de `DECISIONES.md` (no aplica B6, ausencia de dato no es falta).

## Sugerencia de mejora

Reescribir `README.md` con los cinco títulos estándar exigidos por la materia (*Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí*) y corregir la fecha de ejecución de `corridas/corrida_3.md` para que sea coherente con la secuencia temporal del resto del repositorio: es la dimensión donde más puntos se perdieron (D3, 8/15) y el contenido de fondo ya está — solo falta el envase correcto.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

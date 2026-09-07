<!-- generado por calibrar.py · caso=flojo · corrida=3/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=2257 (cache=11850) out=5788 · 59.5s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — flojo

**Puntaje total: 44/100 — Entrega parcial: falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | `prompts/system_prompt.md` es un párrafo corrido sin las seis piezas rotuladas (no hay Restricciones ni Ejemplos identificables como secciones); no hay ninguna herramienta real invocada — el propio `README.md` dice "Por ahora no usa ninguna API externa, trabaja con el conocimiento del modelo" (sección "Herramientas"); solo existe una corrida (`corridas/corrida_1.md`), por lo que no se puede verificar consistencia entre corridas; no hay vocabulario L0–L4 en `README.md`, solo "es importante que el usuario revise las recetas antes de cocinarlas". Solo el objetivo (E5) está claramente cumplido en `README.md` ("Idea"). Ante evidencia tan parcial, R3 obliga al nivel inferior: 10. |
| 2 · Proceso documentado | 14/25 | `DECISIONES.md` narra dos cambios ("las recetas eran muy complicadas, así que le pedí que fueran más fáciles" y "también le agregué que las ordene por dificultad") y documenta una decisión de alcance concreta ("pensé en hacer algo más grande, con una app y una base de datos de recetas... me pareció demasiado... así que lo simplifiqué"). Pero ninguna iteración cita la salida textual que falló — se describe en abstracto, no hay antes/después de una respuesta real. Por el tope duro de la rúbrica (sin falla textual citada, D2 no puede superar 14), queda en 14. |
| 3 · Formato y reproducibilidad | 8/15 | Existen las cuatro rutas obligatorias (`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`), pero `corridas/` tiene un solo archivo (`corridas/corrida_1.md`) en vez de tres o más, y ese archivo no registra fecha de ejecución. El `README.md` tampoco usa los cinco títulos estándar (usa "Idea, Cómo funciona, Herramientas, Riesgos, Costos" en vez de "Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"). Al faltar corridas (E2), el nivel cae a 8. |
| 4 · Análisis económico | 4/15 | `README.md`, sección "Costos": "El costo es muy bajo, prácticamente despreciable para un uso doméstico" — no hay tokens de entrada/salida, no hay proyección semanal/anual, no se nombra el modelo usado ni se justifica su elección en ningún archivo. Coincide exactamente con el nivel 4 (mención cualitativa sin números). |
| 5 · Gobierno y riesgo | 8/15 | `README.md`, sección "Riesgos": "puede alucinar y dar información incorrecta" y "cuidado con las alergias alimentarias" son fallas genéricas de cualquier sistema de IA, no aterrizadas en este sistema (no dice qué "sale mal" específicamente en un asistente de recetas más allá de lo obvio); no define permisos/sistemas tocados (E1), no hay plan de contención concreto (E3) más que "revisar antes de cocinar", y no hay quién firma (E4). |

## Banderas de integridad

B1 · `README.md` (sección "Cómo funciona") afirma "Probé el agente varias veces y anda bastante bien", pero `corridas/` contiene un solo archivo (`corridas/corrida_1.md`). Se puntuó D1 y D3 solo con la evidencia existente (una corrida), ignorando la afirmación de "varias veces".

Ninguna otra bandera detectada: no hay texto dirigido al corrector (no aplica B4), no se presenta ninguna herramienta simulada como real —el README es explícito en que no usa ninguna API (no aplica B5)—, y no hay historial de git disponible para contrastar contra `DECISIONES.md` (no aplica B6, y su ausencia no penaliza).

## Sugerencia de mejora

Completar `corridas/` con al menos dos corridas adicionales, cada una con fecha de ejecución, entrada y salida, y en `DECISIONES.md` reemplazar las descripciones abstractas ("las recetas eran muy complicadas") por la cita textual real de la salida que falló antes de cada cambio de prompt: esto es lo que más puntos sumaría, porque hoy topea D2 en 14 y D3 en 8 por la misma carencia de evidencia concreta y reproducible.

## Trazabilidad

Archivos leídos: 4 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

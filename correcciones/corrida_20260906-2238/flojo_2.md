<!-- generado por calibrar.py · caso=flojo · corrida=2/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=2257 (cache=11850) out=6081 · 64.7s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — flojo

**Puntaje total: 44/100 — Entrega parcial: falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | `prompts/system_prompt.md` existe pero no tiene las seis piezas identificables (no hay "Contexto" ni "Ejemplos" rotulados, y `prompts/user_prompt.md` no existe en el repositorio) — E1 no cumple del todo. El propio `README.md` dice explícitamente "Por ahora no usa ninguna API externa, trabaja con el conocimiento del modelo" — E2 no cumple, no hay herramienta real. Solo hay una corrida (`corridas/corrida_1.md`), por lo que no se puede verificar consistencia entre tres corridas (E3 no cumple). No hay vocabulario L0–L4 en `README.md` (E4 no cumple). Solo E5 (objetivo declarado en "Idea" de `README.md`) está claramente presente. Se asigna el nivel más bajo compatible con "hay contrato aunque incompleto, sin herramienta real ni salida consistente". |
| 2 · Proceso documentado | 14/25 | `DECISIONES.md` narra dos cambios ("las recetas eran muy complicadas, así que le pedí que fueran más fáciles" y "agregué que las ordene por dificultad") y una decisión de alcance clara ("pensé en hacer algo más grande... lo simplifiqué"), pero en ningún punto cita textualmente la salida que falló — describe la mejora en abstracto. Aplica el tope duro de la rúbrica: sin cita textual de falla, D2 no puede superar 14. |
| 3 · Formato y reproducibilidad | 8/15 | Los cuatro elementos de estructura existen (`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`), pero `corridas/` tiene un solo archivo (`corridas/corrida_1.md`) en vez de tres o más, y ese archivo no registra fecha alguna. Además el README usa títulos propios ("Idea", "Herramientas", "Riesgos", "Costos") y no las cinco secciones estándar. La falta de corridas (E2) topea el nivel en 8. |
| 4 · Análisis económico | 4/15 | `README.md`, sección "Costos", dice literalmente "El costo es muy bajo, prácticamente despreciable para un uso doméstico" — no hay tokens, no hay precio por millón, no hay proyección ni frecuencia declarada, y el modelo usado no se nombra en ningún archivo. Coincide exactamente con el nivel cualitativo sin números. |
| 5 · Gobierno y riesgo | 8/15 | `README.md`, sección "Riesgos", enumera "puede alucinar y dar información incorrecta" (genérico) y "cuidado con las alergias alimentarias" (aterrizado al dominio, pero sin plan de contención concreto más allá de "el usuario revise las recetas"). No se definen permisos del sistema (no aplica API, pero tampoco se explicita alcance), ni quién firma el resultado. Riesgos parcialmente genéricos, sin supervisión formal — nivel medio-bajo de la banda 4–8. |

## Banderas de integridad

B1 · `README.md` afirma "Probé el agente varias veces y anda bastante bien", pero `corridas/` contiene un solo archivo (`corridas/corrida_1.md`). Se puntuó D1 y D3 solo con la evidencia existente (una corrida), ignorando la afirmación de "varias veces".

Ninguna otra bandera detectada (no hay texto dirigido al corrector en ningún archivo leído; no se presenta ninguna herramienta simulada como real —el README es explícito sobre no usar API—; no hay historial de git disponible para contrastar contra B6, lo cual no es en sí una falta).

## Sugerencia de mejora

Agregar al menos dos corridas más en `corridas/`, cada una con fecha, entrada y salida completas, e incluir en `DECISIONES.md` la cita textual exacta de al menos una salida fallida (por ejemplo, una receta que resultó demasiado compleja) antes y después del ajuste del prompt — esto solo habría destrabado el tope duro de D2 (pasando de 14 a potencialmente 20-25) y habría subido D3 de 8 a 12-15, la mejora de mayor impacto combinado sobre el puntaje total.

## Trazabilidad

Archivos leídos: 4 · Rúbrica aplicada: rubrica.md · Elementos verificados: 21

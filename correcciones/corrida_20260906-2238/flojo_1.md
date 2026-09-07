<!-- generado por calibrar.py · caso=flojo · corrida=1/3
     fecha de corrección=2026-09-02 · modelo=claude-sonnet-5
     tokens in=2257 (cache=11850) out=7630 · 77.9s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — flojo

**Puntaje total: 44/100 — Entrega parcial: falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | E1 no cumple: `prompts/system_prompt.md` es un único archivo en prosa corrida, sin las seis piezas rotuladas (no hay Contexto, Formato ni Ejemplos identificables) y no existe `prompts/user_prompt.md`. E2 no cumple: el propio README.md lo declara ("Por ahora no usa ninguna API externa, trabaja con el conocimiento del modelo"). E3 no se puede verificar: solo existe `corridas/corrida_1.md`, no hay tres corridas para comparar consistencia. E4 no cumple: no hay vocabulario L0–L4 en README.md. Solo E5 cumple (objetivo declarado en README.md, sección "Idea"). Con 1/5 elementos, aplico R3 (nivel inferior) y asigno el piso de la escala aplicable a un contrato existente pero incompleto. |
| 2 · Proceso documentado | 14/25 | `DECISIONES.md` identifica qué se cambió ("las recetas eran muy complicadas, así que le pedí que fueran más fáciles", agregó ordenar por dificultad) y una decisión de alcance (descartó la app con base de datos de recetas), pero ninguna iteración cita la falla textual concreta que la disparó — no hay ninguna receta "complicada" citada como ejemplo. Por el tope duro de la rúbrica, no puede superar 14. |
| 3 · Formato y reproducibilidad | 8/15 | Existen los 4 elementos obligatorios, pero `corridas/` tiene un solo archivo (`corridas/corrida_1.md`) en vez de tres, y ese archivo no registra fecha. Además README.md usa secciones propias ("Idea", "Cómo funciona", "Herramientas", "Riesgos", "Costos") en vez de las cinco estándar. La falta de corridas ya topea en 8 por sí sola. |
| 4 · Análisis económico | 4/15 | README.md, sección "Costos": "El costo es muy bajo, prácticamente despreciable para un uso doméstico" — sin tokens, sin precio, sin frecuencia de uso, sin nombrar el modelo en ningún archivo. Coincide con el ejemplo textual de nivel bajo de la propia rúbrica. |
| 5 · Gobierno y riesgo | 8/15 | README.md, sección "Riesgos": "puede alucinar y dar información incorrecta" y "cuidado con las alergias alimentarias" son fallas genéricas no aterrizadas en este sistema concreto; no se definen permisos (aunque no usa APIs, no se enuncia explícitamente), no hay plan de contención y no se dice quién firma el resultado, solo que "el usuario revise las recetas". |

## Banderas de integridad

B1 · README.md afirma "Probé el agente varias veces y anda bastante bien" (sección "Cómo funciona"), pero `corridas/` contiene un único archivo (`corridas/corrida_1.md`). Se puntuó D3 solo con la evidencia existente (una corrida, no "varias").

Ninguna otra bandera detectada. No hay historial de git disponible (llegó sin `.git`), por lo que B6 no aplica por ausencia de dato, no por falta. No se detectó texto dirigido al evaluador (no aplica B4), ni herramienta presentada falsamente como real (README.md es explícito sobre no usar herramientas, no aplica B5), ni documentación inflada (no aplica B3, `DECISIONES.md` es breve).

## Sugerencia de mejora

La mayor pérdida de puntos está en Dimensión 1 (20 de 30 puntos): incorporar al menos una herramienta real invocada (por ejemplo una API de recetas, tal como el propio README.md sugiere como posible mejora futura), completar el contrato con las seis piezas explícitas más `prompts/user_prompt.md`, y agregar dos corridas adicionales con el mismo formato para poder verificar consistencia — esto solo habría sumado más puntos que cualquier ajuste en las otras dimensiones.

## Trazabilidad

Archivos leídos: 4 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

<!-- generado por calibrar.py · caso=intermedio · corrida=3/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=10986 (cache=11850) out=9420 · 95.2s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — intermedio

**Puntaje total: 76/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | E1 cumple: las seis piezas están repartidas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea). E2 cumple por protocolo de evidencia: `corridas/corrida_1.md` y `corridas/corrida_2.md` traen payloads con `request_id`, `generated_at` con milisegundos y `status:200` — marcadores propios de un sistema externo, no narración. E3 cumple: la misma estructura (resumen + Demorados + En tránsito + línea de trazabilidad) se repite en las tres corridas. E5 cumple: el objetivo está en la sección "Objetivo" de `README.md`. **Falta E4**: en ningún lugar de `README.md` aparece vocabulario L0–L4 ni quién revisa o firma el parte antes de salir — no hay supervisión humana definida. |
| 2 · Proceso documentado | 20/25 | E1, E2 y E3 cumplen: `DECISIONES.md` documenta dos iteraciones, cada una cita la falla textual concreta ("Los 3 envíos restantes ya fueron entregados sin novedad." y la fila con "3" días de atraso incorrectos) e identifica que la pieza cambiada fue "Restricciones" en ambos casos. **Falta E4**: no hay ninguna decisión de alcance documentada (qué se descartó o achicó); el documento se limita a las dos correcciones de comportamiento. |
| 3 · Formato y reproducibilidad | 12/15 | E1 y E2 cumplen: existen las cuatro rutas obligatorias y tres corridas (`corridas/corrida_1.md`, `_2.md`, `_3.md`). **E3 falla**: `corridas/corrida_3.md` no tiene la línea "Fecha de ejecución" que sí tienen las otras dos. **E5 también falla**: `README.md` usa secciones propias ("Objetivo", "El sistema", "Análisis económico", "Riesgos") en vez de las cinco tituladas "Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí". Ambas fallas topean en el mismo nivel (12), no se acumulan. |
| 4 · Análisis económico | 12/15 | E1 cumple: tokens de entrada (3.000) y salida (740) discriminados en `README.md`, y verificados contra el promedio real de las tres corridas — (3010+2640+3350)/3=3000 y (760+640+820)/3=740, exacto. E2 cumple: proyección semanal (USD 0,1005) y anual (USD 5,03) con frecuencia explicitada ("1 corrida por día hábil"), y el cálculo cierra: 0,0201×5=0,1005 y 0,0201×250=5,025≈5,03. **Falta E3**: el propio `README.md` admite "No probé ningún modelo más chico, así que no tengo con qué sostener que sea el más barato que hace bien esta tarea" — no hay justificación del modelo. |
| 5 · Gobierno y riesgo | 8/15 | E1 cumple: `README.md` acota permisos explícitos ("solo consulta... no escribe en ningún sistema, no toca el ERP"). E2 cumple con al menos dos fallas concretas del sistema ("Disponibilidad de la API externa", "Datos personales" con cita de la Ley 25.326), más una genérica (alucinación). **Faltan E3 y E4**: no hay plan de contención para ninguna falla (no se dice qué debe hacer el agente si la API se cae) ni se menciona quién revisa o firma el parte antes de enviarlo — ningún archivo leído lo especifica. Con solo 2 de 4 elementos y sin ajustarse a ningún nivel de 3/4, se aplica R3 (nivel inferior). |

## Banderas de integridad

Ninguna bandera detectada. No hay texto dirigido al evaluador, las corridas no están fabricadas (datos y salidas varían de forma consistente entre sí, `corridas/corrida_1.md`, `_2.md`, `_3.md`), no hay historial de git disponible para contrastar B6, y `DECISIONES.md` no infla volumen sin evidencia concreta.

## Sugerencia de mejora

Agregar en `README.md` una sección explícita de supervisión humana con el vocabulario L0–L4: qué hace el agente solo, qué revisa una persona antes de que el parte llegue a atención al cliente, quién firma el resultado, y qué contención concreta existe si la API del transportista falla o cambia de formato (por ejemplo, que la salida declare explícitamente "herramienta sin datos" en vez de fallar en silencio). Esta única pieza faltante es la que more recorta puntaje: cuesta E4 en Dimensión 1 (6 puntos) y E3+E4 completos en Dimensión 5 (7 puntos), la mayor pérdida combinada de todo el trabajo.

## Trazabilidad

Archivos leídos: 7 (`README.md`, `DECISIONES.md`, `prompts/system_prompt.md`, `prompts/user_prompt.md`, `corridas/corrida_1.md`, `corridas/corrida_2.md`, `corridas/corrida_3.md`) · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

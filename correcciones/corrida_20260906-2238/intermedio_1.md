<!-- generado por calibrar.py · caso=intermedio · corrida=1/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=10986 (cache=11850) out=14238 · 144.2s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — intermedio

**Puntaje total: 76/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | Las seis piezas del contrato están repartidas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea) — E1 cumple. E2 cumple con evidencia fuerte: `corridas/corrida_1.md` y `corridas/corrida_2.md` traen la respuesta cruda de `consultar_envios` con `request_id`, `generated_at` con milisegundos y `status: 200`, marcadores de sistema externo real, no simulado. E3 cumple: las tres corridas comparten el mismo esqueleto (resumen, tabla Demorados, tabla En tránsito, línea de trazabilidad). E5 cumple: el objetivo está declarado en `README.md` ("Objetivo"). **E4 no cumple**: no hay ninguna mención al vocabulario L0–L4 ni a quién revisa o firma el resultado en `README.md`. 4 de 5 elementos con E1 y E2 presentes → nivel 24. |
| 2 · Proceso documentado | 20/25 | `DECISIONES.md` documenta dos iteraciones con antes/después reales: Iteración 1 cita textual "Los 3 envíos restantes ya fueron entregados sin novedad." y el campo `estado` real que la contradice; Iteración 2 cita la fila exacta con el atraso mal contado. Ambas identifican la pieza cambiada (Restricciones) y el texto agregado — E1, E2, E3 cumplen. **E4 no cumple**: `DECISIONES.md` no documenta ninguna decisión de alcance (qué se achicó o descartó); el README menciona de pasada que "el sistema no reemplaza a nadie" pero eso no es una decisión de alcance documentada en `DECISIONES.md` como pide la rúbrica. 3 de 4 con E2 presente → nivel 20. |
| 3 · Formato y reproducibilidad | 12/15 | Las cuatro rutas obligatorias existen y hay tres corridas (E1, E2 cumplen). **E3 falla**: `corridas/corrida_3.md` no registra fecha de ejecución en ningún encabezado (a diferencia de `corridas/corrida_1.md` y `corridas/corrida_2.md`, que sí la tienen), y su bloque de respuesta tampoco trae `generated_at`. **E5 falla**: `README.md` usa "Objetivo", "El sistema", "Análisis económico", "Riesgos" — no las cinco secciones estándar exigidas ("Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"). Cualquiera de las dos fallas topea en 12. |
| 4 · Análisis económico | 12/15 | E1 cumple: cada corrida anota tokens de entrada/salida al pie (`corridas/corrida_1.md`: 3.010/760; `corrida_2.md`: 2.640/640; `corrida_3.md`: 3.350/820), promediados en `README.md`. E2 cumple: proyección semanal y anual con frecuencia explícita ("1 corrida por día hábil"). E4 cumple: recalculado, 3.000×3/1.000.000 + 740×15/1.000.000 = USD 0,0201 por corrida, ×5 = USD 0,1005 semanal, ×250 = USD 5,03 anual — coincide exactamente con lo declarado en `README.md`, y el promedio de tokens (3.000/740) coincide con el promedio real de las tres corridas. **E3 no cumple**: el propio `README.md` admite "No probé ningún modelo más chico... Es una cuenta que me quedó sin hacer" — no hay justificación del modelo bajo el criterio del curso. 3 de 4 con proyección presente pero sin justificación de modelo → nivel 12. |
| 5 · Gobierno y riesgo | 8/15 | E1 cumple con precisión: `README.md` acota permisos a "solo consulta la API del transportista con la cuenta VETRO-4471: no escribe en ningún sistema, no toca el ERP". E2 es parcial: solo un riesgo está aterrizado en este sistema ("si el servicio del transportista se cae o cambia el formato de la respuesta, el parte del día puede salir mal o no salir"), mientras "Alucinación" se enuncia en términos genéricos ("Como todo sistema basado en un modelo de lenguaje, puede inventar información"), igual al ejemplo de nivel bajo de la rúbrica. **E3 no cumple**: no hay ningún plan de contención descrito para ninguno de los riesgos listados en `README.md`. **E4 no cumple**: no se menciona en ningún archivo quién revisa la salida antes de confiar en ella ni quién firma el parte. Con dos elementos completamente ausentes y uno parcial, aplica R3 (nivel inferior) → nivel 8. |

## Banderas de integridad

Ninguna bandera detectada. La revisión de `corridas/` muestra datos crudos con marcadores de sistema externo genuinos (request_id, timestamps con milisegundos, status codes) que respaldan tanto E2 de D1 como los totales agregados de D4 (B5 y B2b no aplican). `DECISIONES.md` cita fallas textuales concretas, no aplica B3. No se detectó texto dirigido al evaluador en ningún archivo (no aplica B4). No hay historial de git disponible en esta entrega, por lo que B6 no es evaluable (no es una falta en sí misma).

## Sugerencia de mejora

La mayor pérdida de puntos está en Dimensión 5 (7 puntos) y se solapa con la falla de E4 en Dimensión 1: agregar en `README.md` una sección explícita de supervisión humana usando el vocabulario L0–L4 (qué corre solo el agente, qué revisa una persona antes de que el parte salga, quién firma la presentación) y, junto a cada riesgo ya listado, un plan de contención concreto (por ejemplo, qué hace el sistema si `consultar_envios` devuelve un error o cambia de formato) — esta única mejora sumaría puntos simultáneamente en D1 (E4) y D5 (E3, E4), que es donde más evidencia falta hoy.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

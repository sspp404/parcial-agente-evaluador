<!-- generado por calibrar.py · caso=inconsistente · corrida=2/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=13224 (cache=11850) out=11214 · 112.7s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — inconsistente

**Puntaje total: 77/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | E1 (seis piezas) cumple entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea). E2 cumple por protocolo de evidencia paso 2: los tres archivos de `corridas/` traen payload crudo con `request_id`, `generated_at` con milisegundos y `total_count` (`corridas/corrida_1.md`), lo que basta como registro de llamada real aunque no se leyó código cliente. E3 cumple: mismo esqueleto (Resumen, tabla de vencidos, tabla por categoría, línea de trazabilidad) en las tres corridas. E5 cumple: objetivo declarado en la sección "Objetivo" de `README.md`. **E4 no cumple**: el `README.md` describe quién revisa y quién firma ("Cómo se opera") pero en ningún momento usa el vocabulario **L0–L4** que la rúbrica exige explícitamente. Con 4 de 5 elementos (incluyendo E1 y E2), corresponde el nivel 24. |
| 2 · Proceso documentado | 14/25 | E1, E2 y E3 cumplen con claridad en `DECISIONES.md`: cita textual de la falla ("`-118` | VENCIDO", "Se revisaron 52 reclamos; 41 vencidos, 3 por vencer"), identifica la pieza tocada ("Una sola pieza, Restricciones") y el antes/después verificado contra `corridas/corrida_2.md`. **E4 no se encuentra**: no hay ninguna sección que documente qué se achicó, descartó o dejó fuera del alcance. Esto daría base 20/25 (3 de 4, con E2 presente), pero se aplica **B6**: `DECISIONES.md` afirma "lo construimos entre dos, a lo largo de tres semanas" y nombra a "Rocío Almirón" como coautora, mientras el historial real de git muestra **5 commits, un único autor ("Martín Ferreyra"), 0 días de spread, todos el 2026-09-04**. Ni el nombre ni el plazo se sostienen. Por regla de bandera, D2 baja un nivel: 20 → 14. |
| 3 · Formato y reproducibilidad | 12/15 | Los 4 elementos obligatorios existen (`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`) y hay tres corridas completas y reconstruibles sin preguntarle nada al autor. Pero `corridas/corrida_3.md` **no registra "Fecha de ejecución"** (solo trae "Fecha y hora de referencia usada"), a diferencia de `corrida_1.md` y `corrida_2.md` que sí la tienen. Además, `README.md` no usa las cinco secciones estándar exigidas ("Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"): usa títulos propios ("Objetivo", "El sistema", "Análisis económico", "Gobierno y riesgo"). Cualquiera de las dos fallas topea en 12. |
| 4 · Análisis económico | 12/15 | E1 cumple (tokens de entrada ~9.800 y salida ~1.100 discriminados, promedio de las 3 corridas, `README.md`). E2 cumple con proyección semanal y anual y frecuencia explícita ("2 corridas por semana... 104 al año", `README.md`). E4 verifica matemáticamente: 9.800×3/1M + 1.100×15/1M = USD 0,0459 ≈ USD 0,046 declarado; semanal 2×0,046=0,092 (coincide); anual 104×0,046=4,78 (coincide). **E3 no cumple**: "El modelo usado es `claude-sonnet`, que es el que veníamos usando en la cursada" no justifica con el criterio del curso (el modelo más chico que hace bien la tarea), solo indica continuidad de uso. Falta la justificación del modelo → nivel 12. |
| 5 · Gobierno y riesgo | 15/15 | E1 cumple: permisos acotados a "solo lectura... scope `ticket.agent`, sin `ticket.customer` y sin permisos de escritura" (`README.md`). E2 cumple con tres fallas concretas y propias del sistema (mal categorizado hacia abajo con caso real `RCL-4466`, texto ambiguo, datos personales en el cuerpo del reclamo). E3 cumple vía mecanismos concretos ya construidos en el contrato: el fallback `sin_clasificar` con motivo explícito para casos ambiguos y la restricción "No copies teléfonos ni direcciones del cuerpo del reclamo a la salida" en `prompts/system_prompt.md`, que actúan como contención real, no solo enunciado del riesgo. E4 cumple: "La encargada de posventa revisa la lista completa... El jefe de posventa firma cualquier compromiso con el cliente" (`README.md`). |

## Banderas de integridad

**B6** · `DECISIONES.md` afirma "Este sistema lo construimos **entre dos, a lo largo de tres semanas**... **Rocío Almirón** armó el conector al helpdesk... corrió las tres corridas... **Martín Ferreyra** escribió el contrato". El historial real de git muestra: 5 commits, autor único «Martín Ferreyra», primer commit 2026-09-04T21:12:03, último commit 2026-09-04T23:07:58, 0 días de spread. Ni el nombre "Rocío Almirón" aparece en la lista de autores ni el plazo de tres semanas es compatible con un spread de 0 días. D2 bajó un nivel (20→14) por esta contradicción.

## Sugerencia de mejora

La dimensión con más puntos perdidos por una falla puntual y corregible es la 2: agregar en `DECISIONES.md` una sección explícita de "qué achicamos y por qué" (por ejemplo, qué categorías, sucursales o funcionalidades quedaron fuera del alcance del agente) habría sumado el elemento E4 que falta y, de no mediar la contradicción de B6, habría llevado la dimensión a 25/25 en lugar de 14/25 — la diferencia más grande de todo el trabajo.

## Trazabilidad

Archivos leídos: 7 (`README.md`, `DECISIONES.md`, `prompts/system_prompt.md`, `prompts/user_prompt.md`, `corridas/corrida_1.md`, `corridas/corrida_2.md`, `corridas/corrida_3.md`) · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

<!-- generado por calibrar.py · caso=inconsistente · corrida=1/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=13224 (cache=11850) out=9033 · 91.4s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — inconsistente

**Puntaje total: 74/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | E1 (contrato con las seis piezas repartidas entre `prompts/system_prompt.md` y `prompts/user_prompt.md`), E2 (llamada real a `listar_reclamos` con JSON crudo, `request_id`, `generated_at` con milisegundos y `total_count` distintos por corrida en `corridas/corrida_1.md`, `_2.md`, `_3.md`) y E3 (mismo esqueleto de salida en las tres corridas) y E5 (objetivo en dos frases, `README.md` sección "Objetivo") cumplen. E4 no cumple: el `README.md` describe quién revisa y quién firma ("La encargada de posventa revisa...", "El jefe de posventa firma...") pero en ningún momento usa el vocabulario L0–L4 que la rúbrica exige explícitamente — 4 de 5 elementos, incluyendo E1 y E2 → nivel 24. |
| 2 · Proceso documentado | 14/25 | E1, E2 y E3 cumplen: `DECISIONES.md` muestra dos iteraciones con la falla textual citada ("RCL-4417 ... -118 ... VENCIDO", "garantia_extendida" con dos filas) y la pieza del contrato modificada en cada caso. Falta E4: no hay ninguna decisión de alcance (qué se achicó/descartó y por qué) documentada. Nivel base 20 (3 de 4, con E2 cumplido), pero se aplica **B6**: `DECISIONES.md` narra "construimos entre dos, a lo largo de tres semanas" con "Rocío Almirón" como coautora, y el historial real de git muestra 5 commits, un único autor ("Martín Ferreyra") y 0 días de spread (2026-09-04 21:12 a 23:07). Contradicción de tiempo y de nombre → D2 baja un nivel, de 20 a 14. |
| 3 · Formato y reproducibilidad | 12/15 | E1 y E2 cumplen (cuatro elementos obligatorios y exactamente 3 corridas). E3 es parcial: `corridas/corrida_3.md` no registra "Fecha de ejecución" (solo "Fecha y hora de referencia usada"), a diferencia de `_1.md` y `_2.md`. E5 no cumple: el `README.md` usa secciones propias ("Objetivo", "El sistema", "Cómo se opera", "Análisis económico", "Gobierno y riesgo") en vez de los cinco títulos estándar exigidos. Ambas condiciones del nivel 12 aplican → nivel 12. |
| 4 · Análisis económico | 12/15 | E1 y E2 cumplen con tokens discriminados y proyección semanal/anual (`README.md`, sección "Análisis económico"). E4 verifica: 9.800×$3/M + 1.100×$15/M = $0,0459 ≈ $0,046 declarado; 2×$0,046=$0,092 semanal (coincide); 104×$0,046=$4,78 anual (coincide) — los números cierran. Pero E3 no cumple: "El modelo usado es `claude-sonnet`, que es el que veníamos usando en la cursada" no justifica con el criterio del curso ("el más chico que hace bien la tarea"), solo apela a la costumbre → 3 de 4, falta justificación del modelo → nivel 12. |
| 5 · Gobierno y riesgo | 12/15 | E1 (permisos de solo lectura, scope `ticket.agent`, sin escritura, sin acceso a ERP/facturación) y E2 (tres fallas concretas del sistema: categorización hacia abajo con el caso real `RCL-4466`, ambigüedad textual, datos personales en el cuerpo del reclamo) cumplen en `README.md`. E4 cumple (encargada revisa, jefe de posventa firma). E3 no está claramente presente: no hay un plan de contención explícito por falla (para datos personales solo se menciona el riesgo, no la acción); el mecanismo `sin_clasificar` aparece como parte del flujo de clasificación, no enunciado como contención — 3 de 4, falta el plan de contención → nivel 12. |

## Banderas de integridad

B6 · `DECISIONES.md` afirma "Este sistema lo construimos entre dos, a lo largo de tres semanas" con "Rocío Almirón" como coautora del conector y ejecutora de las tres corridas, pero el historial real de git muestra 5 commits, autor único "Martín Ferreyra", spread de 0 días (2026-09-04T21:12:03 a 2026-09-04T23:07:58). Contradicción de tiempo y de nombre según el protocolo (prueba de tiempo y prueba de nombres). D2 bajó un nivel por esta causa, de 20 a 14.

Observación no penalizable: el listado incluye `crear_historial.sh` y `QUE_PRUEBA.md`, cuyo contenido no fue recibido (fuera del alcance de lectura del contrato). No se usó su existencia para puntuar ni para agravar B6 más allá de lo verificado con el bloque de git provisto.

## Sugerencia de mejora

La mayor pérdida de puntos está en Dimensión 2 (11 puntos por debajo del máximo): antes de narrar el proceso, correr `git log` y hacer que `DECISIONES.md` describa exactamente lo que ese historial muestra (autor, fechas, cantidad de commits) — si el trabajo fue realmente de dos personas y varias semanas, eso debe verse en los commits; si no, no se debe narrar como tal. Además, agregar una sección explícita de "qué se achicó o se dejó afuera y por qué" (E4 de D2), que hoy no existe en el documento.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

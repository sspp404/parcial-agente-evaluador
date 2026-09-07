<!-- generado por calibrar.py · caso=inconsistente · corrida=3/3
     fecha de corrección=2026-09-06 · modelo=claude-sonnet-5
     tokens in=13224 (cache=11850) out=12133 · 128.1s
     stop_reason=end_turn · veredicto de formato=ok
     SALIDA SIN EDITAR -->


# Corrección — inconsistente

**Puntaje total: 74/100 — Sólido con huecos identificables**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 24/30 | E1 cumple: las seis piezas están repartidas entre `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea). E2 cumple con evidencia fuerte: las tres corridas pegan la respuesta cruda de la API con `request_id`, `generated_at` con milisegundos y `total_count` (`corridas/corrida_1.md`, `corridas/corrida_2.md`, `corridas/corrida_3.md`), satisfaciendo el paso 2 del protocolo E2. E3 cumple: mismo esqueleto en las tres corridas. E5 cumple: objetivo declarado en `README.md` ("Objetivo"). **E4 no cumple**: la sección "Cómo se opera" de `README.md` describe quién revisa y quién firma en prosa, pero en ningún archivo aparece el vocabulario L0–L4 que la rúbrica exige explícitamente. 4 de 5 elementos con E1 y E2 presentes → nivel 24. |
| 2 · Proceso documentado | 14/25 | E1, E2 y E3 cumplen: `DECISIONES.md` documenta dos iteraciones con la falla textual citada ("RCL-4417 ... -118 ... VENCIDO", "garantia_extendida") y qué pieza del contrato se tocó. **E4 no cumple**: no hay ninguna decisión de alcance (qué se achicó/descartó) en `DECISIONES.md` — la única mención de recorte ("no pegamos los 52 o 38 tickets enteros por largo") está en `README.md`, no en el archivo que exige la rúbrica. Esto da nivel base 20 (3/4 incluyendo E2). **Aplica B6** (ver abajo), que baja un nivel adicional → 14. |
| 3 · Formato y reproducibilidad | 12/15 | Los cuatro elementos obligatorios existen y hay tres corridas (`corridas/corrida_1.md`, `_2.md`, `_3.md`). Pero `corridas/corrida_3.md` no registra "Fecha de ejecución" (solo "Fecha y hora de referencia usada"), a diferencia de las otras dos corridas — falta el dato en una de ellas. Además `README.md` no usa las cinco secciones estándar ("Qué construí · Cómo se lo pedí · Qué funciona · Qué falta o qué falló · Qué aprendí"); usa secciones propias ("Objetivo", "El sistema", "Cómo se opera", etc.). Cualquiera de las dos condiciones topea en 12. |
| 4 · Análisis económico | 12/15 | E1 (tokens de entrada/salida discriminados, `README.md` "Análisis económico"), E2 (proyección semanal y anual con frecuencia explícita: "2 corridas por semana... = 104 al año") y E4 (los números cierran: 9.800×3/1e6 + 1.100×15/1e6 = USD 0,0459 ≈ 0,046 declarado; ×2 = 0,092 semanal declarado; ×104 = 4,78 anual declarado — todo consistente) cumplen. **E3 no cumple**: la justificación del modelo no usa el criterio del curso ("el más chico que hace bien la tarea"); el texto dice solo "es el que veníamos usando en la cursada" (`README.md`, sección "Análisis económico"), que es inercia, no el criterio pedido. 3/4 elementos, falta justificación del modelo → nivel 12. |
| 5 · Gobierno y riesgo | 12/15 | E1 cumple con detalle concreto (scope `ticket.agent`, sin `ticket.customer`, sin escritura, `README.md` "Qué toca y con qué permisos"). E2 cumple con tres fallas específicas del sistema, incluyendo una que realmente ocurrió (`RCL-4466` en `corridas/corrida_3.md`). E4 cumple ("Quién revisa y quién firma": encargada revisa, jefe de posventa firma). **E3 (plan de contención) es débil/ambiguo**: para el riesgo de datos personales no hay ningún plan de contención descrito (solo una restricción de no copiar datos a la salida, que es prevención, no contención), y no hay plan explícito para caída de la API. Por R3 se trata como ausente → 3/4, falta plan de contención → nivel 12. |

## Banderas de integridad

- **B6 · Historial de commits inconsistente con el relato.** `DECISIONES.md` afirma "Este sistema lo construimos entre dos, a lo largo de tres semanas" y atribuye a "Rocío Almirón" la construcción del conector al helpdesk y la corrida de las tres corridas. El historial real de git muestra **5 commits, un único autor ("Martín Ferreyra"), 0 días de spread entre el primero (2026-09-04T21:12:03) y el último (2026-09-04T23:07:58)**. Ni el nombre "Rocío Almirón" aparece en la lista de autores, ni el proceso de tres semanas es compatible con 0 días de spread. Se aplicó la prueba de tiempo y la prueba de nombres del protocolo: ambas contradicen el relato. D2 bajó un nivel (de 20 a 14) por esta contradicción.

Ninguna otra bandera detectada: no hay texto dirigido al corrector (no B4), no hay señales de herramienta simulada (los payloads JSON con `request_id` y timestamps en milisegundos sostienen E2 como invocación real, no B5), no hay fechas imposibles ni corridas fabricadas (B2a/B2b no aplican — los tres archivos de `corridas/` tienen entrada, respuesta cruda y salida propias y distintas entre sí), y no hay afirmaciones del README sin respaldo en archivo (B1 no aplica).

## Sugerencia de mejora

La dimensión con más puntos perdidos en términos absolutos es Proceso documentado (11 puntos). La mejora de mayor impacto es resolver la contradicción B6: si el trabajo fue hecho por una sola persona en una sesión de trabajo concentrada, `DECISIONES.md` debería narrar eso — no un proceso de tres semanas con una coautora que no aparece en el historial de git — y agregar en ese mismo archivo (no solo en el README) una sección explícita de "qué achicamos y por qué" (por ejemplo, la decisión de no pegar los tickets completos por extensión). Corregir ambas cosas recupera un nivel completo en D2 (de 14 a 20).

## Trazabilidad

Archivos leídos: 7 (`README.md`, `DECISIONES.md`, `prompts/system_prompt.md`, `prompts/user_prompt.md`, `corridas/corrida_1.md`, `corridas/corrida_2.md`, `corridas/corrida_3.md`) · Rúbrica aplicada: rubrica.md · Elementos verificados: 22

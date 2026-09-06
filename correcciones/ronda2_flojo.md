# Corrección — casos/flojo (Asistente de recetas)

*Ronda 2 · rúbrica v2 · fecha de corrección 2026-09-04 · salida sin editar*

**Puntaje total: 44/100 — Entrega parcial: falta al menos una dimensión entera**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 10/30 | Hay contrato escrito pero incompleto: `prompts/system_prompt.md` tiene Rol ("Sos un asistente de cocina"), Tarea y algunas restricciones, pero no tiene Contexto ni Ejemplos rotulados y no existe `prompts/user_prompt.md` (E1 parcial). E2 ausente: el propio `README.md` (sección Herramientas) dice "no usa ninguna API externa" y no hay ningún registro de llamada en `corridas/`. E3 no verificable: `corridas/` contiene un solo archivo, no se puede comprobar consistencia entre tres corridas. E4 ausente: no aparece el vocabulario L0–L4 ni quién firma en `README.md`. E5 presente: objetivo declarado en `README.md` (sección Idea). Corresponde el nivel "solo contrato sin herramienta real ni salida estructurada consistente" |
| 2 · Proceso documentado | 14/25 | `DECISIONES.md` identifica dos cambios al contrato ("le pedí que fueran más fáciles", "le agregué que las ordene por dificultad", verificables contra `prompts/system_prompt.md`) y una decisión de alcance real ("pensé en hacer algo más grande, con una app y una base de datos de recetas... lo simplifiqué") — E1 parcial, E3 parcial, E4 presente. E2 ausente: ninguna falla textual citada; la mejora se describe en abstracto ("hasta que las respuestas me gustaron", "quedó mejor"). Se aplica el tope duro de la dimensión (máximo 14) por ausencia total de falla citada |
| 3 · Formato y reproducibilidad | 8/15 | E1 presente: existen `README.md`, `prompts/`, `corridas/` y `DECISIONES.md`. E2 ausente: hay una sola corrida (`corridas/corrida_1.md`), faltan dos. E3 ausente: `corridas/corrida_1.md` registra entrada y salida pero no tiene fecha. E4 parcial: no consta qué versión del prompt se usó ni cuándo — evidencia insuficiente. Corresponde el nivel "faltan corridas" |
| 4 · Análisis económico | 4/15 | `README.md` (sección Costos) dice "El costo es muy bajo, prácticamente despreciable para un uso doméstico": mención cualitativa sin ningún número. No hay tokens de entrada/salida discriminados (E1), ni proyección semanal/anual con supuesto de frecuencia (E2), ni justificación del modelo elegido (E3) — de hecho no se nombra ningún modelo en ningún archivo del repositorio |
| 5 · Gobierno y riesgo | 8/15 | `README.md` (sección Riesgos) enuncia los riesgos en términos genéricos: "Como todo sistema de IA, puede alucinar y dar información incorrecta" y una mención a alergias alimentarias sin aterrizarla en el sistema construido (E2 parcial). E3 ausente: no hay plan de contención, solo el riesgo. E4 parcial: dice "es importante que el usuario revise las recetas antes de cocinarlas" pero no define quién firma. E1 ausente: no se declaran sistemas tocados ni permisos en ningún archivo |

## Banderas de integridad

B1 · `README.md` (sección Cómo funciona) afirma "Probé el agente varias veces y anda bastante bien", pero `corridas/` contiene un único archivo (`corridas/corrida_1.md`). Se puntuaron D1 y D3 solo con la evidencia existente; por R6 el descuento se aplicó una sola vez, en D1.

B1 · `README.md` (sección Costos) afirma "El costo es muy bajo, prácticamente despreciable" sin ningún archivo que respalde el cálculo. D4 se puntuó solo con la evidencia existente.

No se detectaron B2a, B2b, B3, B4 ni B5. En particular, no hay herramienta simulada presentada como real: `README.md` declara explícitamente que no usa API externa, lo cual es honesto y evita B5.

## Sugerencia de mejora

La dimensión 1 es donde más puntos se perdieron (20). El cambio de mayor rendimiento es conectar una herramienta real al agente —por ejemplo la API de recetas que el propio `README.md` menciona como pendiente, o incluso una búsqueda web— y registrar en cada corrida la llamada completa: qué herramienta se invocó, con qué parámetros exactos y qué devolvió; y hacerlo en tres corridas con entradas distintas, misma estructura de salida y fecha. Eso solo levantaría D1 de 10 a hasta 30 y D3 de 8 a hasta 15.

## Trazabilidad

Archivos leídos: 4 · Rúbrica aplicada: rubrica.md · Elementos verificados: 21

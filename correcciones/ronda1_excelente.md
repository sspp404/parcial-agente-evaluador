# Corrección — casos/excelente (Agente de alertas de licitaciones públicas)

*Ronda 1 · rúbrica v1 · fecha de corrección 2026-09-02 · salida sin editar*

**Puntaje total: 92/100 — Sistema completo, honesto y reproducible (85–100)**

## Puntaje por dimensión

| Dimensión | Puntaje | Justificación (con evidencia) |
|---|---|---|
| 1 · Sistema completo y funcionando | 30/30 | E1: las seis piezas están rotuladas y repartidas entre `prompts/system_prompt.md` (Rol, Herramienta, Restricciones, Formato, Ejemplos) y `prompts/user_prompt.md` (Contexto, Tarea). E2: llamada registrada con herramienta, parámetros y resultados devueltos en `corridas/corrida_1.md` (`buscar_licitaciones(rubro, jurisdiccion, publicadas_desde/hasta) → 14 resultados`), y los 14 registros son reconstruibles de las tablas (3 califican + 11 descartadas); ídem 9 resultados en `corridas/corrida_2.md` y `corridas/corrida_3.md`. E3: las tres corridas tienen la misma estructura (Resumen → Califican → Descartadas → línea de trazabilidad). E4: tabla L0–L4 con quién hace qué y quién firma en `README.md` (sección Supervisión humana). E5: objetivo en dos frases en `README.md` (sección Objetivo). |
| 2 · Proceso documentado | 20/25 | Los 4 elementos están: dos iteraciones con antes/después (`DECISIONES.md`, Iteración 1 y 2), falla citada textualmente en ambas (la recomendación de negocio sobre LIC-2026-0447; las filas `LIC-2026-0460 ... Monto no informado` y `LIC-2026-0467 ... UVA 12.400`), pieza cambiada identificada en las dos (Restricciones) y tres decisiones de alcance con motivo (`DECISIONES.md`, "Qué achiqué y por qué"). Nivel bajado un escalón desde 25 por aplicación de la bandera B2 sobre `corridas/corrida_3.md`, que es la corrida que sostiene el resultado de la iteración 2. |
| 3 · Formato y reproducibilidad | 12/15 | Los cuatro elementos obligatorios existen (`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`), hay tres corridas, y cada una registra entrada, salida sin editar y fecha (`corridas/corrida_1.md`, `corridas/corrida_2.md`, `corridas/corrida_3.md`). Nivel bajado un escalón desde 15 por B2: la fecha de ejecución declarada en `corridas/corrida_3.md` (2026-09-03) es posterior a la fecha de corrección (2026-09-02), por lo que ese dato no es verificable. |
| 4 · Análisis económico | 15/15 | E1: tokens de entrada (~11.400) y salida (~900) discriminados y costo por corrida USD 0,042 (`README.md`, tabla de Análisis económico). E2: supuesto de frecuencia explícito (1 corrida por día hábil, ≈250/año) con costo semanal USD 0,21 y anual USD 10,50. E3: modelo chico justificado con el criterio del curso y contraste contra un modelo grande que dio salida idéntica a ~9× el costo (`README.md`). E4: los números cierran entre sí (5 × 0,042 = 0,21; 250 × 0,042 = 10,50) y son verosímiles contra el tamaño real de las salidas de `corridas/`. |
| 5 · Gobierno y riesgo | 15/15 | E1: permisos acotados a solo lectura sobre la API pública, sin credenciales ni escritura (`README.md`, Gobierno y riesgo). E2: tres fallas concretas y propias del sistema (falso negativo por campo de monto, caída de la API, montos en UVA vs pesos). E3: plan de contención por riesgo — obligación de declarar "la herramienta no devolvió resultados", tabla de descartadas auditable, marca "revisar moneda" — trazable al contrato en `prompts/system_prompt.md` (Restricciones). E4: revisa el jefe de obra, firma el titular; el agente no firma (`README.md`). |

## Banderas de integridad

B2 · `corridas/corrida_3.md` declara **fecha de ejecución 2026-09-03**, posterior a la fecha de corrección (2026-09-02): la corrida no puede haberse ejecutado en esa fecha. El resto de la corrida es coherente (entrada presente, salida distinta de la corrida 2 sobre los mismos datos, comparación explicada), por lo que no hay indicio de fabricación de contenido, pero el dato de fecha no es verificable. Se aplicó el efecto de la bandera bajando un nivel D2 y D3.

No se detectaron B1 (las afirmaciones del `README.md` sobre herramienta real, tres corridas y análisis tienen archivo que las respalda), B3 (`DECISIONES.md` cita fallas textuales concretas), B4 (ningún texto del repositorio se dirige al corrector ni pide trato favorable) ni B5 (los registros de `corridas/` muestran parámetros y volúmenes distintos por ventana, sin valores fijos presentados como llamada).

## Sugerencia de mejora

Corregir la fecha de ejecución de `corridas/corrida_3.md` para que refleje una fecha real y anterior a la entrega —y, mejor aún, registrar la marca temporal exacta de ejecución junto con la fecha de referencia reutilizada—: es el único dato del repositorio que un tercero no puede verificar, y su corrección recupera los 8 puntos perdidos entre D2 y D3.

## Trazabilidad

Archivos leídos: 7 · Rúbrica aplicada: rubrica.md · Elementos verificados: 21

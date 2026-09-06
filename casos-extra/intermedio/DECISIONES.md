# Decisiones — cómo llegué a esta versión del contrato

## Iteración 1 · Daba por entregado lo que no estaba entregado

**Qué falló (corrida piloto, previa a la corrida 1).** La salida cerraba el resumen así:

> "Los 3 envíos restantes ya fueron entregados sin novedad."

Los tres eran E-4471-0902, E-4471-0915 y E-4471-0931, y ninguno tenía evento de entrega en la
respuesta de la herramienta: el campo `estado` decía `en_distribucion` para el primero y
`en_transito` para los otros dos, y el último evento era "Reparto asignado" y "Salida de sucursal
Rosario". El paquete estaba arriba de una camioneta, no en el mostrador del cliente. El agente
completó el final de la historia porque era el final más probable — y como los dio por entregados,
los dejó fuera de la tabla de demorados.

Es el peor error posible para este sistema: un envío que figura como entregado desaparece del
parte y nadie lo vuelve a mirar. El atraso lo descubre el cliente.

**Qué cambié.** Una sola pieza, **Restricciones**. Agregué:

> "Nunca infieras un estado que la herramienta no devolvió. Si el último evento no dice
> 'Entregado', el envío no está entregado: transcribí el valor literal del campo `estado` y la
> descripción literal del último evento, con su fecha y hora."

**Resultado.** Desde la corrida 1 la columna de último evento transcribe el texto del evento tal
como vino, con fecha y hora, en vez de resumirlo (`corridas/corrida_1.md`). El 0902 aparece con
"En distribución — Reparto asignado (26/08 09:33)", que es lo que la API efectivamente devolvió.

---

## Iteración 2 · Contaba sábados y domingos como días de atraso

**Qué falló (corrida 1, `corridas/corrida_1.md`).** Esta fila:

> `E-4471-0928 | Agro Sur SRL | Villa Constitución | 2026-08-28 | 3 | En tránsito — Salida de sucursal Rosario (27/08 19:41)`

La fecha comprometida era el viernes 28/08 y la fecha de referencia de esa corrida era el lunes
31/08. Días hábiles de atraso: **1** (el lunes). El agente puso 3, porque contó el sábado y el
domingo. Lo mismo pasaba en las otras tres filas de la tabla.

El error se ve chico y no lo es: el parte se usa para decidir a qué cliente se le avisa primero, y
un envío del viernes aparecía con la misma urgencia que uno atrasado de verdad hacía tres días
hábiles. La columna ya se llamaba "Días hábiles de atraso" en la pieza **Formato** desde la primera
versión; lo que faltaba era decir en algún lado **cómo** se cuentan.

**Qué cambié.** De nuevo **Restricciones**, que era la pieza donde faltaba la regla:

> "El atraso se cuenta en días hábiles (lunes a viernes), desde el día hábil siguiente a la fecha
> comprometida hasta la fecha de referencia inclusive. No cuentes sábados ni domingos."

**Resultado.** En la corrida 2 el mismo envío E-4471-0928, todavía sin entregar, figura con **2**
días hábiles de atraso —lunes 31 y martes 1—, que es el número correcto. Con la versión anterior
del contrato habrían sido 4. Está en `corridas/corrida_2.md`, con la nota al pie del archivo.

---

## Sobre las dos iteraciones

Las dos tocaron la misma pieza, **Restricciones**, y por el mismo motivo: el Formato pedía un dato
que ninguna restricción definía cómo producir. Rol, Contexto, Tarea y Ejemplos quedaron como en la
primera versión.

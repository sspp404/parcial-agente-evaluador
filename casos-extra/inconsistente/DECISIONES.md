# Decisiones — cómo llegamos acá

## Cómo trabajamos

Este sistema lo construimos **entre dos, a lo largo de tres semanas**. Arrancamos el **11 de
agosto** con la primera versión del contrato y la cerramos la primera semana de septiembre,
después de tres corridas y dos reescrituras del system prompt.

El reparto fue así: **Rocío Almirón** armó el conector al helpdesk —conseguir el token de solo
lectura con el área de sistemas, entender el esquema de tickets de Zammad, dejar la llamada
`listar_reclamos` funcionando— y corrió las tres corridas contra la instancia real de Casa
Bertoldi. **Martín Ferreyra** escribió el contrato (las dos versiones), revisó las salidas contra
la planilla de la encargada de posventa y escribió este documento.

Las dos iteraciones que siguen salieron de sesiones de revisión conjunta, mirando la salida de la
corrida anterior en pantalla partida contra la planilla que la encargada venía llenando a mano.
Entre la corrida 1 y la corrida 2 pasó casi una semana, porque tuvimos que esperar a que sistemas
nos habilitara el token con el scope correcto.

---

## Iteración 1 · Todas las horas daban negativas

**Qué falló (corrida 1, ver `corridas/corrida_1.md`).** La salida marcó **41 de 52 reclamos como
vencidos**, con las horas en negativo. Primera fila de la tabla, textual:

> `RCL-4417 | Rosario Centro | garantia | Heladera Gafa HGF-350L | -118 | VENCIDO | Falla dentro del período de garantía`

Y el resumen decía:

> "Se revisaron 52 reclamos; 41 vencidos, 3 por vencer."

Recalculamos a mano contra la fecha de referencia del contexto (2026-08-17 09:00): `RCL-4417`
había entrado el 2026-08-14 a las 18:02, o sea **63 horas**, no -118. Y `RCL-4426`, con 24 horas
sobre un SLA de 72, estaba tranquilamente en plazo y aparecía como vencido. Los vencidos reales
eran **6**.

El agente estaba restando contra su propia noción de "hoy" en vez de contra la fecha de referencia
que le pasamos en el contexto. Una lista donde el 79% de los reclamos figura vencido no es una
lista de prioridades: es ruido, y la encargada la iba a descartar en la primera reunión.

**Qué cambiamos.** Una sola pieza, **Restricciones**. Agregamos:

> "Calculá las horas transcurridas de cada reclamo contra la **fecha y hora de referencia** que te
> da el contexto, nunca contra la fecha de tu sistema."

**Resultado.** En la corrida 2 las horas dieron bien: verificamos tres a mano contra el campo
`created_at` de la respuesta cruda y coincidieron. Los vencidos pasaron de 41 a 4.

---

## Iteración 2 · Se inventó una quinta categoría

**Qué falló (corrida 2, ver `corridas/corrida_2.md`).** Aparecieron dos reclamos con una categoría
que no existe:

> `RCL-4459 | Fisherton | garantia_extendida | Aire Surrey 3300F | 51 | VENCIDO | Falla cubierta por la garantía extendida contratada aparte`
> `RCL-4462 | Funes | garantia_extendida | Lavarropas Drean Next 8.12 | 47 | POR VENCER | Falla cubierta por la garantía extendida contratada aparte`

Y el resumen por categoría salió con **cinco filas** en vez de cuatro:

> `garantia | 15 | 1` · `logistica | 11 | 2` · `facturacion | 6 | 0` · `uso | 4 | 0` · `garantia_extendida | 2 | 1`

Visto de afuera parece un detalle prolijo —el agente notó que esos dos clientes tenían garantía
extendida, que es cierto y está en el texto del reclamo—, pero rompe lo único que hace útil al
resumen: la planilla de posventa tiene cuatro categorías fijas y se compara semana contra semana.
Con una categoría de más, la encargada no puede pegar el resultado; tiene que reclasificar a mano,
que es exactamente el trabajo que veníamos a sacarle.

Lo que nos preocupó no fue la categoría inventada en sí, sino qué hace el agente cuando un reclamo
no le encaja: en vez de decirlo, se inventa un casillero. Ese mismo impulso, en un reclamo
ambiguo, lo mete en la categoría más parecida y nadie se entera.

**Qué cambiamos.** Dos piezas, **Restricciones** y **Formato**:

> "Clasificá cada reclamo en **una sola** de estas cuatro categorías, escritas exactamente así:
> `garantia`, `logistica`, `facturacion`, `uso`. **No inventes categorías nuevas ni variantes.**
> Si ninguna de las cuatro encaja, usá `sin_clasificar` y explicá en la columna de motivo qué te
> falta para decidir. Un reclamo `sin_clasificar` no tiene SLA: poné `SIN SLA` en la columna
> Estado y listalo igual en la tabla de fuera de plazo, para que alguien lo mire."

**Resultado.** Corrimos la corrida 3 sobre exactamente los mismos 38 reclamos de la corrida 2 para
poder comparar (ver `corridas/corrida_3.md`). Los dos `garantia_extendida` volvieron a `garantia`.
Y salió un efecto que no habíamos previsto: `RCL-4466` —"vino fallado", con la caja abierta, que
puede ser falla de fábrica o golpe del flete— pasó de estar escondido en `uso` a salir como
`sin_clasificar` con el motivo escrito. La corrida 2 lo había clasificado mal en silencio. El
cambio no solo sacó la categoría inventada: hizo visible una duda que antes el agente se tragaba.

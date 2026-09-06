# Agente de triage de reclamos de posventa — Casa Bertoldi

**Trabajo final · Programación de y con Agentes de IA · MBA UCEMA**

Autor: Martín Ferreyra

## Objetivo

Dos veces por semana (lunes y jueves), leer todos los reclamos de posventa que entraron al
helpdesk de Casa Bertoldi —distribuidora de electrodomésticos, seis sucursales en Rosario y el
cordón— clasificarlos en las cuatro categorías con las que trabaja el área y marcar cuáles están
fuera del SLA de respuesta, para que la reunión de posventa empiece con la lista ya hecha.

Hoy eso lo hace la encargada de posventa a mano: abre el helpdesk, lee reclamo por reclamo y
arma la planilla. Le lleva entre 50 y 70 minutos cada vez, y los reclamos vencidos aparecen
cuando el cliente vuelve a escribir enojado, no antes.

## El sistema

- **Contrato:** `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) +
  `prompts/user_prompt.md` (Contexto, Tarea).
- **Herramienta real:** la API del helpdesk (Zammad, instancia propia de la empresa). El agente
  arma la consulta con la ventana de fechas del contexto, la ejecuta y trabaja sobre los tickets
  que devuelve. En cada archivo de `corridas/` está pegada, sin editar, la respuesta cruda de esa
  llamada: el encabezado completo (`request_id`, `generated_at`, `query`, `total_count`) más los
  primeros tickets del arreglo. No pegamos los 52 o 38 tickets enteros por largo; los que están,
  están tal cual volvieron.
- **Salida estructurada:** tabla de reclamos fuera de SLA o por vencer + tabla resumen por
  categoría + línea de trazabilidad con la consulta usada.
- **Corridas:** tres, en `corridas/`, con la entrada, la respuesta cruda de la herramienta y la
  salida sin editar.

## Las cuatro categorías

| Categoría | Qué entra | SLA de respuesta |
|---|---|---|
| `garantia` | El producto falla dentro del período de garantía | 48 h |
| `logistica` | Entrega demorada, dañada en el traslado, dirección equivocada | 24 h |
| `facturacion` | Factura mal emitida, nota de crédito, cobro duplicado | 72 h |
| `uso` | El producto anda, el cliente no sabe usarlo o esperaba otra cosa | 72 h |

Son las mismas cuatro con las que la encargada arma la planilla desde antes del agente. No las
inventamos nosotros: las copiamos de su planilla para que el resultado se pueda comparar contra
lo que ella venía haciendo.

## Cómo se opera

La encargada de posventa corre el agente el lunes y el jueves a la mañana, y lleva la lista a la
reunión de las 10. Antes de comprometer una respuesta con el cliente, revisa el reclamo en el
helpdesk. El jefe de posventa firma cualquier compromiso comercial con el cliente (cambio de
producto, nota de crédito, envío sin cargo): el agente no escribe nada en ningún sistema y no
contesta ningún reclamo.

## Análisis económico

Medido sobre las tres corridas de `corridas/`, con los precios del modelo usado
(USD 3 por millón de tokens de entrada, USD 15 por millón de tokens de salida):

| Concepto | Valor |
|---|---|
| Tokens de entrada por corrida (promedio de las 3) | ~9.800 |
| Tokens de salida por corrida (promedio de las 3) | ~1.100 |
| Costo por corrida | USD 0,046 |
| Frecuencia declarada | 2 corridas por semana (lunes y jueves) = 104 al año |
| Costo semanal | USD 0,092 |
| Costo anual (104 corridas) | USD 4,78 |

El modelo usado es `claude-sonnet`, que es el que veníamos usando en la cursada.

Contra eso: la encargada dedica ~2 horas por semana a armar la planilla, unas 100 horas al año.
El agente no la reemplaza —sigue revisando reclamo por reclamo antes de responder—, le saca la
parte de leer 40 tickets para encontrar los 6 que están vencidos.

## Gobierno y riesgo

**Qué toca y con qué permisos.** Un token de la API del helpdesk con permiso de **solo lectura**
sobre el listado de tickets (scope `ticket.agent`, sin `ticket.customer` y sin permisos de
escritura). No puede responder, cerrar, reasignar ni editar un ticket. No accede al ERP, ni a la
facturación, ni a datos de tarjeta: los reclamos de `facturacion` traen el número de factura,
nunca el medio de pago.

**Qué puede salir mal.**

1. *Reclamo mal categorizado hacia abajo.* Un reclamo de `logistica` (SLA 24 h) clasificado como
   `uso` (SLA 72 h) desaparece de la lista de vencidos por dos días. Nos pasó en la corrida 2 con
   `RCL-4466`: quedó en `uso` sin decir nada, y recién en la corrida 3 salió como
   `sin_clasificar` (ver `corridas/corrida_3.md` y `DECISIONES.md`, iteración 2).
2. *Reclamo textualmente ambiguo.* "Vino fallado" puede ser garantía o daño en el traslado, y la
   diferencia son 24 horas de SLA. El texto del cliente no siempre alcanza para decidir.
3. *Datos personales en el cuerpo del reclamo.* Los clientes escriben teléfono y a veces dirección
   dentro del texto del ticket, y eso viaja al modelo en cada corrida.

**Quién revisa y quién firma.** La encargada de posventa revisa la lista completa antes de la
reunión y es la que decide qué se contesta primero. El jefe de posventa firma cualquier
compromiso con el cliente. El agente no firma nada y no le escribe a ningún cliente.

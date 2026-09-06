# Corrida 3

**Fecha y hora de referencia usada:** 2026-08-20 09:00 (se repitió a propósito la ventana de la
corrida 2, para comparar el efecto de la iteración 2 sobre exactamente los mismos reclamos)
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión final)

## Entrada

Mismo user prompt y misma ventana que la corrida 2 —referencia 2026-08-20 09:00, desde
2026-08-17 09:00, las seis sucursales— con el system prompt corregido por la iteración 2.

## Llamada a la herramienta

```
listar_reclamos(
  desde="2026-08-17T09:00:00-03:00",
  hasta="2026-08-20T09:00:00-03:00",
  estado="abierto"
)
→ 38 resultados
```

## Respuesta cruda de la herramienta (misma ventana que la corrida 2, a propósito)

```json
{
  "request_id": "req_8bf5107a34d9",
  "generated_at": "2026-08-20T11:47:33.512Z",
  "query": {"desde": "2026-08-17T09:00:00-03:00", "hasta": "2026-08-20T09:00:00-03:00", "estado": "abierto"},
  "total_count": 38,
  "page": 1,
  "per_page": 50,
  "tickets": [
    {
      "number": "RCL-4459",
      "created_at": "2026-08-18T08:40:55.019Z",
      "group": "Fisherton",
      "channel": "web_form",
      "title": "Split que no arranca",
      "article_body": "El aire Surrey 3300F lo compré en diciembre con la garantía extendida de 2 años que me vendieron en el mostrador. No arranca la unidad exterior.",
      "state": "new"
    },
    {
      "number": "RCL-4462",
      "created_at": "2026-08-18T13:00:41.663Z",
      "group": "Funes",
      "channel": "email",
      "title": "Lavarropas pierde agua",
      "article_body": "El Drean Next 8.12 pierde agua por abajo. Lo compré hace 5 meses y le pagué aparte la extensión de garantía.",
      "state": "new"
    },
    {
      "number": "RCL-4466",
      "created_at": "2026-08-19T11:52:08.337Z",
      "group": "Roldán",
      "channel": "whatsapp",
      "title": "Vino fallado",
      "article_body": "Buenas, el horno eléctrico vino fallado. No sé si ya venía así o se golpeó en el camión, la caja estaba abierta.",
      "state": "new"
    }
  ]
}
```

El `request_id` y el `generated_at` son distintos —es otra llamada, hecha la misma mañana un rato
después—, pero `total_count` y los tickets son los mismos que en la corrida 2: la ventana que se
pide es la misma (`desde` y `hasta` fijos en la consulta, no relativos a "ahora"), así que la
herramienta devuelve exactamente los mismos 38 reclamos. Se repitió a propósito para aislar el
efecto del cambio de contrato.

## Salida (sin editar)

Se revisaron 38 reclamos; 4 vencidos, 2 por vencer, 1 sin clasificar.

### Fuera de plazo o por vencer

| ID | Sucursal | Categoría | Producto | Horas | Estado | Motivo de la categoría |
|---|---|---|---|---|---|---|
| RCL-4455 | Villa Gobernador Gálvez | logistica | Cocina Escorial Candor 56 | 68 | VENCIDO | Daño producido en el traslado, no falla del producto |
| RCL-4468 | Granadero Baigorria | logistica | Heladera Patrick HPK136 | 31 | VENCIDO | Entrega no realizada en la ventana pactada |
| RCL-4457 | Rosario Centro | garantia | Microondas Whirlpool WM1811D | 51 | VENCIDO | Falla dentro del período de garantía |
| RCL-4459 | Fisherton | garantia | Aire Surrey 3300F | 51 | VENCIDO | Falla del producto; la extensión contratada aparte no cambia la categoría |
| RCL-4451 | Roldán | facturacion | Termotanque Rheem 85L | 71 | POR VENCER | Nota de crédito no emitida sobre factura A 0006-00012802 |
| RCL-4462 | Funes | garantia | Lavarropas Drean Next 8.12 | 47 | POR VENCER | Falla del producto; la extensión contratada aparte no cambia la categoría |
| RCL-4466 | Roldán | sin_clasificar | Horno eléctrico Ariston FA3 | 21 | SIN SLA | No puedo decidir entre `garantia` y `logistica`: el cliente dice "vino fallado" y que la caja estaba abierta. Falta saber si el daño es de fábrica o del traslado |

### Resumen por categoría

| Categoría | Cantidad | Vencidos |
|---|---|---|
| garantia | 17 | 2 |
| logistica | 11 | 2 |
| facturacion | 6 | 0 |
| uso | 3 | 0 |
| sin_clasificar | 1 | 0 |

Herramienta: listar_reclamos · consulta: desde=2026-08-17T09:00, hasta=2026-08-20T09:00, estado=abierto · resultados: 38 · referencia: 2026-08-20 09:00.

---

**Comparación contra la corrida 2 (mismos 38 reclamos).** Desapareció la categoría inventada: los
dos reclamos que estaban en `garantia_extendida` (`RCL-4459` y `RCL-4462`) volvieron a `garantia`,
que es donde la encargada los carga en su planilla. Y apareció algo que no esperábamos: `RCL-4466`,
que la corrida 2 había metido en `uso` sin decir nada, ahora sale como `sin_clasificar` con el
motivo escrito. Es el reclamo que en la corrida 2 estaba mal clasificado y nadie lo iba a notar.

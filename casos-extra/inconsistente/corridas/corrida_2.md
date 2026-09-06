# Corrida 2

**Fecha de ejecución:** 2026-08-20
**Fecha y hora de referencia usada:** 2026-08-20 09:00
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (con la iteración 1 aplicada,
sin la iteración 2 — ver `DECISIONES.md`)

## Entrada

User prompt completado con: referencia 2026-08-20 09:00, ventana desde 2026-08-17 09:00 (la
corrida anterior), las seis sucursales, las cuatro categorías de la planilla. Los reclamos los
trajo la herramienta.

## Llamada a la herramienta

```
listar_reclamos(
  desde="2026-08-17T09:00:00-03:00",
  hasta="2026-08-20T09:00:00-03:00",
  estado="abierto"
)
→ 38 resultados
```

## Respuesta cruda de la herramienta (muestra — el resto sigue el mismo esquema)

```json
{
  "request_id": "req_4d02b8ce7731",
  "generated_at": "2026-08-20T09:02:16.884Z",
  "query": {"desde": "2026-08-17T09:00:00-03:00", "hasta": "2026-08-20T09:00:00-03:00", "estado": "abierto"},
  "total_count": 38,
  "page": 1,
  "per_page": 50,
  "tickets": [
    {
      "number": "RCL-4455",
      "created_at": "2026-08-17T15:40:12.774Z",
      "group": "Villa Gobernador Gálvez",
      "channel": "whatsapp",
      "title": "Cocina entregada con la puerta rayada",
      "article_body": "Llegó la cocina Escorial Candor 56 y la puerta del horno vino toda rayada de un lado. El flete se fue sin que la revisáramos.",
      "state": "new"
    },
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
    }
  ]
}
```

## Salida (sin editar)

Se revisaron 38 reclamos; 4 vencidos, 2 por vencer.

### Fuera de plazo o por vencer

| ID | Sucursal | Categoría | Producto | Horas | Estado | Motivo de la categoría |
|---|---|---|---|---|---|---|
| RCL-4455 | Villa Gobernador Gálvez | logistica | Cocina Escorial Candor 56 | 68 | VENCIDO | Daño producido en el traslado, no falla del producto |
| RCL-4468 | Granadero Baigorria | logistica | Heladera Patrick HPK136 | 31 | VENCIDO | Entrega no realizada en la ventana pactada |
| RCL-4457 | Rosario Centro | garantia | Microondas Whirlpool WM1811D | 51 | VENCIDO | Falla dentro del período de garantía de fábrica |
| RCL-4459 | Fisherton | garantia_extendida | Aire Surrey 3300F | 51 | VENCIDO | Falla cubierta por la garantía extendida contratada aparte |
| RCL-4451 | Roldán | facturacion | Termotanque Rheem 85L | 71 | POR VENCER | Nota de crédito no emitida sobre factura A 0006-00012802 |
| RCL-4462 | Funes | garantia_extendida | Lavarropas Drean Next 8.12 | 47 | POR VENCER | Falla cubierta por la garantía extendida contratada aparte |

### Resumen por categoría

| Categoría | Cantidad | Vencidos |
|---|---|---|
| garantia | 15 | 1 |
| logistica | 11 | 2 |
| facturacion | 6 | 0 |
| uso | 4 | 0 |
| garantia_extendida | 2 | 1 |

Herramienta: listar_reclamos · consulta: desde=2026-08-17T09:00, hasta=2026-08-20T09:00, estado=abierto · resultados: 38 · referencia: 2026-08-20 09:00.

---

**Observación registrada al revisar esta corrida.** Las horas ahora dan bien (verificamos tres a
mano contra `created_at`). Pero aparecieron dos reclamos con la categoría `garantia_extendida`,
que **no existe** en la planilla de posventa: son cuatro categorías, no cinco. La encargada no
puede pegar este resumen en su planilla porque tiene una fila de más. Esto disparó la iteración 2
(ver `DECISIONES.md`).

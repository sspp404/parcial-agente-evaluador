# Corrida 1

**Fecha de ejecución:** 2026-08-17
**Fecha y hora de referencia usada:** 2026-08-17 09:00
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión inicial, anterior a
la iteración 1 — ver `DECISIONES.md`)

## Entrada

User prompt completado con: referencia 2026-08-17 09:00, ventana desde 2026-08-13 09:00, las seis
sucursales, las cuatro categorías de la planilla. No se pegó ningún reclamo: los trajo la
herramienta.

## Llamada a la herramienta

```
listar_reclamos(
  desde="2026-08-13T09:00:00-03:00",
  hasta="2026-08-17T09:00:00-03:00",
  estado="abierto"
)
→ 52 resultados
```

## Respuesta cruda de la herramienta (muestra — el resto sigue el mismo esquema)

```json
{
  "request_id": "req_a91c3f7b2e04",
  "generated_at": "2026-08-17T09:03:41.226Z",
  "query": {"desde": "2026-08-13T09:00:00-03:00", "hasta": "2026-08-17T09:00:00-03:00", "estado": "abierto"},
  "total_count": 52,
  "page": 1,
  "per_page": 50,
  "tickets": [
    {
      "number": "RCL-4417",
      "created_at": "2026-08-14T18:02:37.481Z",
      "group": "Rosario Centro",
      "channel": "web_form",
      "title": "La heladera no enfría",
      "article_body": "Compré la heladera Gafa HGF-350L en abril y desde el martes no enfría el freezer. Tengo la factura A 0003-00041882.",
      "state": "new"
    },
    {
      "number": "RCL-4421",
      "created_at": "2026-08-15T11:47:09.052Z",
      "group": "Funes",
      "channel": "email",
      "title": "No me llegó el lavarropas",
      "article_body": "Me lo tenían que entregar el jueves entre 8 y 13 y no vino nadie. Nadie avisó nada.",
      "state": "new"
    },
    {
      "number": "RCL-4426",
      "created_at": "2026-08-16T09:15:52.310Z",
      "group": "Roldán",
      "channel": "web_form",
      "title": "Factura duplicada",
      "article_body": "Me facturaron dos veces el mismo microondas, facturas A 0006-00012774 y A 0006-00012781.",
      "state": "new"
    }
  ]
}
```

## Salida (sin editar)

Se revisaron 52 reclamos; 41 vencidos, 3 por vencer.

### Fuera de plazo o por vencer

| ID | Sucursal | Categoría | Producto | Horas | Estado | Motivo de la categoría |
|---|---|---|---|---|---|---|
| RCL-4417 | Rosario Centro | garantia | Heladera Gafa HGF-350L | -118 | VENCIDO | Falla dentro del período de garantía |
| RCL-4421 | Funes | logistica | Lavarropas Drean Next 8.12 | -101 | VENCIDO | Entrega no realizada en la ventana pactada |
| RCL-4426 | Roldán | facturacion | Microondas BGH Quick Chef | -75 | VENCIDO | Doble facturación del mismo producto |
| RCL-4428 | Fisherton | garantia | Anafe Longvie 13512BF | -71 | VENCIDO | Falla dentro del período de garantía |
| RCL-4430 | Granadero Baigorria | logistica | Termotanque Rheem 85L | -68 | VENCIDO | Producto entregado con abolladura |
| … | … | … | … | … | … | … |

*(la tabla siguió con 39 filas más, todas con horas negativas y todas marcadas VENCIDO)*

### Resumen por categoría

| Categoría | Cantidad | Vencidos |
|---|---|---|
| garantia | 21 | 18 |
| logistica | 14 | 12 |
| facturacion | 9 | 7 |
| uso | 8 | 4 |

Herramienta: listar_reclamos · consulta: desde=2026-08-13T09:00, hasta=2026-08-17T09:00, estado=abierto · resultados: 52 · referencia: 2026-08-17 09:00.

---

**Observación registrada al revisar esta corrida.** Todas las horas salieron negativas y 41 de 52
reclamos quedaron marcados `VENCIDO`. Recalculando a mano contra la fecha de referencia
(2026-08-17 09:00), `RCL-4417` entró el 2026-08-14 a las 18:02, o sea **63 horas**, no -118: está
vencido igual, pero la cuenta está mal. Y `RCL-4426` entró el 2026-08-16 09:15 (**24 h** sobre un
SLA de 72) y no está vencido en absoluto. Los vencidos reales eran 6, no 41. Esto disparó la
iteración 1 (ver `DECISIONES.md`).

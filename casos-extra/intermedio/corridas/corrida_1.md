# Corrida 1

**Fecha de ejecución:** 2026-08-31
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión anterior a la
iteración 2 — ver `DECISIONES.md`)

## Entrada

User prompt de la plantilla diaria, sin cambios: cuenta `VETRO-4471`, envíos en curso. No se pegó
ningún listado de envíos; el agente armó y ejecutó la consulta.

## Llamada a la herramienta

```
consultar_envios(
  cuenta="VETRO-4471",
  estado="en_curso"
)
→ 12 resultados
```

## Respuesta de la herramienta (muestra de 3 de los 12 — el resto sigue el mismo esquema)

```json
{
  "request_id": "req_a91c37f5be20",
  "generated_at": "2026-08-31T08:04:52.317Z",
  "status": 200,
  "query": {"cuenta": "VETRO-4471", "estado": "en_curso"},
  "total_results": 12,
  "page": 1,
  "results": [
    {
      "numero_envio": "E-4471-0928",
      "cliente": "Agro Sur SRL",
      "localidad": "Villa Constitución",
      "provincia": "Santa Fe",
      "fecha_despacho": "2026-08-25T16:22:41.000Z",
      "fecha_comprometida": "2026-08-28",
      "estado": "en_transito",
      "ultimo_evento": {
        "fecha": "2026-08-27T19:41:08.000Z",
        "descripcion": "Salida de sucursal Rosario",
        "sucursal": "ROS-01"
      }
    },
    {
      "numero_envio": "E-4471-0902",
      "cliente": "Cabaña La Elvira",
      "localidad": "Firmat",
      "provincia": "Santa Fe",
      "fecha_despacho": "2026-08-24T11:08:19.000Z",
      "fecha_comprometida": "2026-08-26",
      "estado": "en_distribucion",
      "ultimo_evento": {
        "fecha": "2026-08-26T09:33:57.000Z",
        "descripcion": "Reparto asignado",
        "sucursal": "FIR-02"
      }
    },
    {
      "numero_envio": "E-4471-0937",
      "cliente": "Veterinaria del Centro",
      "localidad": "Rosario",
      "provincia": "Santa Fe",
      "fecha_despacho": "2026-08-28T15:47:03.000Z",
      "fecha_comprometida": "2026-09-01",
      "estado": "en_transito",
      "ultimo_evento": {
        "fecha": "2026-08-28T18:12:44.000Z",
        "descripcion": "Ingreso a centro de clasificación",
        "sucursal": "ROS-01"
      }
    }
  ]
}
```

## Salida (sin editar)

Se revisaron 12 envíos en curso; 4 están demorados.

### Demorados

| N° envío | Cliente | Localidad | Comprometida | Días hábiles de atraso | Último evento registrado |
|---|---|---|---|---|---|
| E-4471-0902 | Cabaña La Elvira | Firmat | 2026-08-26 | 5 | En distribución — Reparto asignado (26/08 09:33) |
| E-4471-0915 | Veterinaria San Martín | Casilda | 2026-08-27 | 4 | En tránsito — Arribo a sucursal destino Casilda (28/08 07:12) |
| E-4471-0928 | Agro Sur SRL | Villa Constitución | 2026-08-28 | 3 | En tránsito — Salida de sucursal Rosario (27/08 19:41) |
| E-4471-0931 | Agrovet Pergamino | Pergamino | 2026-08-28 | 3 | En tránsito — Salida de sucursal Rosario (28/08 20:05) |

### En tránsito sin atraso

| N° envío | Cliente | Estado | Comprometida |
|---|---|---|---|
| E-4471-0937 | Veterinaria del Centro | en_transito | 2026-09-01 |
| E-4471-0938 | Agropecuaria Los Molinos | en_transito | 2026-09-01 |
| E-4471-0939 | Veterinaria Belgrano | en_transito | 2026-09-02 |
| E-4471-0941 | Rural Cañada SRL | en_distribucion | 2026-08-31 |
| E-4471-0942 | Veterinaria Sur | en_transito | 2026-09-02 |
| E-4471-0943 | Agroservicios Roldán | en_transito | 2026-09-03 |
| E-4471-0944 | Veterinaria Pichincha | en_transito | 2026-09-03 |
| E-4471-0945 | Estancia El Ombú | en_transito | 2026-09-04 |

Herramienta: consultar_envios · consulta: cuenta=VETRO-4471, estado=en_curso · envíos devueltos: 12.

---

**Tokens (panel de uso):** entrada 3.010 · salida 760.

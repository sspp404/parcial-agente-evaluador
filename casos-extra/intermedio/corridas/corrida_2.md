# Corrida 2

**Fecha de ejecución:** 2026-09-01
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión actual, con la regla
de días hábiles agregada en la iteración 2 — ver `DECISIONES.md`)

## Entrada

Mismo user prompt de la plantilla diaria: cuenta `VETRO-4471`, envíos en curso. Tampoco se pegó
listado; el agente ejecutó la consulta.

## Llamada a la herramienta

```
consultar_envios(
  cuenta="VETRO-4471",
  estado="en_curso"
)
→ 10 resultados
```

## Respuesta de la herramienta (muestra de 3 de los 10 — el resto sigue el mismo esquema)

```json
{
  "request_id": "req_c48d0b7719a3",
  "generated_at": "2026-09-01T08:02:17.884Z",
  "status": 200,
  "query": {"cuenta": "VETRO-4471", "estado": "en_curso"},
  "total_results": 10,
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
        "fecha": "2026-08-31T22:14:36.000Z",
        "descripcion": "Arribo a sucursal Villa Constitución",
        "sucursal": "VCO-01"
      }
    },
    {
      "numero_envio": "E-4471-0941",
      "cliente": "Rural Cañada SRL",
      "localidad": "Cañada de Gómez",
      "provincia": "Santa Fe",
      "fecha_despacho": "2026-08-28T09:15:02.000Z",
      "fecha_comprometida": "2026-08-31",
      "estado": "en_distribucion",
      "ultimo_evento": {
        "fecha": "2026-09-01T06:40:11.000Z",
        "descripcion": "Reparto asignado",
        "sucursal": "CDG-01"
      }
    },
    {
      "numero_envio": "E-4471-0945",
      "cliente": "Estancia El Ombú",
      "localidad": "Bigand",
      "provincia": "Santa Fe",
      "fecha_despacho": "2026-08-31T17:05:29.000Z",
      "fecha_comprometida": "2026-09-04",
      "estado": "en_transito",
      "ultimo_evento": {
        "fecha": "2026-08-31T20:48:13.000Z",
        "descripcion": "Ingreso a centro de clasificación",
        "sucursal": "ROS-01"
      }
    }
  ]
}
```

## Salida (sin editar)

Se revisaron 10 envíos en curso; 3 están demorados.

### Demorados

| N° envío | Cliente | Localidad | Comprometida | Días hábiles de atraso | Último evento registrado |
|---|---|---|---|---|---|
| E-4471-0902 | Cabaña La Elvira | Firmat | 2026-08-26 | 4 | En distribución — Segundo intento de entrega (01/09 07:55) |
| E-4471-0928 | Agro Sur SRL | Villa Constitución | 2026-08-28 | 2 | En tránsito — Arribo a sucursal Villa Constitución (31/08 22:14) |
| E-4471-0941 | Rural Cañada SRL | Cañada de Gómez | 2026-08-31 | 1 | En distribución — Reparto asignado (01/09 06:40) |

### En tránsito sin atraso

| N° envío | Cliente | Estado | Comprometida |
|---|---|---|---|
| E-4471-0937 | Veterinaria del Centro | en_transito | 2026-09-01 |
| E-4471-0938 | Agropecuaria Los Molinos | en_transito | 2026-09-01 |
| E-4471-0939 | Veterinaria Belgrano | en_transito | 2026-09-02 |
| E-4471-0942 | Veterinaria Sur | en_transito | 2026-09-02 |
| E-4471-0943 | Agroservicios Roldán | en_transito | 2026-09-03 |
| E-4471-0944 | Veterinaria Pichincha | en_distribucion | 2026-09-03 |
| E-4471-0945 | Estancia El Ombú | en_transito | 2026-09-04 |

Herramienta: consultar_envios · consulta: cuenta=VETRO-4471, estado=en_curso · envíos devueltos: 10.

---

**Tokens (panel de uso):** entrada 2.640 · salida 640.

**Nota al revisar:** E-4471-0915 y E-4471-0931 ya no aparecen porque se entregaron el 31/08 y
salieron del estado `en_curso`. El 0928 sigue sin entregar y ahora cuenta 2 días hábiles de atraso
(lunes 31 y martes 1), no 4 como habría contado la versión anterior del contrato.

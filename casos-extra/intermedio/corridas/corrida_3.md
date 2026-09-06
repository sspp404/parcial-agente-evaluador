# Corrida 3

**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión actual, la misma de la
corrida 2)

## Entrada

Mismo user prompt de la plantilla diaria: cuenta `VETRO-4471`, envíos en curso. Sin listado pegado;
el agente ejecutó la consulta.

## Llamada a la herramienta

```
consultar_envios(
  cuenta="VETRO-4471",
  estado="en_curso"
)
→ 14 resultados
```

## Respuesta de la herramienta (pegué el bloque de resultados; muestra de 3 de los 14 — el resto sigue el mismo esquema)

```json
[
  {
    "numero_envio": "E-4471-0902",
    "cliente": "Cabaña La Elvira",
    "localidad": "Firmat",
    "provincia": "Santa Fe",
    "fecha_despacho": "2026-08-24T11:08:19.000Z",
    "fecha_comprometida": "2026-08-26",
    "estado": "en_distribucion",
    "ultimo_evento": {
      "fecha": "2026-09-03T07:20:14.000Z",
      "descripcion": "Tercer intento de entrega",
      "sucursal": "FIR-02"
    }
  },
  {
    "numero_envio": "E-4471-0949",
    "cliente": "Agropecuaria San Genaro",
    "localidad": "San Genaro",
    "provincia": "Santa Fe",
    "fecha_despacho": "2026-09-01T10:33:50.000Z",
    "fecha_comprometida": "2026-09-02",
    "estado": "en_transito",
    "ultimo_evento": {
      "fecha": "2026-09-03T05:12:29.000Z",
      "descripcion": "Demora por corte de ruta 34",
      "sucursal": "ROS-01"
    }
  },
  {
    "numero_envio": "E-4471-0951",
    "cliente": "Agro Insumos Totoras",
    "localidad": "Totoras",
    "provincia": "Santa Fe",
    "fecha_despacho": "2026-09-03T09:41:07.000Z",
    "fecha_comprometida": "2026-09-07",
    "estado": "en_transito",
    "ultimo_evento": {
      "fecha": "2026-09-03T11:58:44.000Z",
      "descripcion": "Ingreso a centro de clasificación",
      "sucursal": "ROS-01"
    }
  }
]
```

## Salida (sin editar)

Se revisaron 14 envíos en curso; 5 están demorados.

### Demorados

| N° envío | Cliente | Localidad | Comprometida | Días hábiles de atraso | Último evento registrado |
|---|---|---|---|---|---|
| E-4471-0902 | Cabaña La Elvira | Firmat | 2026-08-26 | 6 | En distribución — Tercer intento de entrega (03/09 07:20) |
| E-4471-0937 | Veterinaria del Centro | Rosario | 2026-09-01 | 2 | En tránsito — Arribo a sucursal Rosario (02/09 20:11) |
| E-4471-0939 | Veterinaria Belgrano | Rosario | 2026-09-02 | 1 | En distribución — Reparto asignado (03/09 06:35) |
| E-4471-0942 | Veterinaria Sur | Rosario | 2026-09-02 | 1 | En tránsito — Salida de sucursal Rosario (02/09 19:48) |
| E-4471-0949 | Agropecuaria San Genaro | San Genaro | 2026-09-02 | 1 | En tránsito — Demora por corte de ruta 34 (03/09 05:12) |

### En tránsito sin atraso

| N° envío | Cliente | Estado | Comprometida |
|---|---|---|---|
| E-4471-0943 | Agroservicios Roldán | en_transito | 2026-09-03 |
| E-4471-0944 | Veterinaria Pichincha | en_distribucion | 2026-09-03 |
| E-4471-0945 | Estancia El Ombú | en_transito | 2026-09-04 |
| E-4471-0948 | Veterinaria Fisherton | en_transito | 2026-09-04 |
| E-4471-0950 | Veterinaria Alberdi | en_transito | 2026-09-04 |
| E-4471-0951 | Agro Insumos Totoras | en_transito | 2026-09-07 |
| E-4471-0952 | Veterinaria Arroyito | en_transito | 2026-09-07 |
| E-4471-0953 | Cabaña Don Aldo | en_transito | 2026-09-08 |
| E-4471-0954 | Veterinaria La Paz | en_transito | 2026-09-08 |

Herramienta: consultar_envios · consulta: cuenta=VETRO-4471, estado=en_curso · envíos devueltos: 14.

---

**Tokens (panel de uso):** entrada 3.350 · salida 820.

**Nota al revisar:** E-4471-0928, E-4471-0938 y E-4471-0941 ya no figuran porque se entregaron y
salieron del estado `en_curso`. El 0902 lleva tres intentos de entrega fallidos: es el caso que
más justifica el parte, porque a mano no lo veía nadie hasta que llamaba el cliente.

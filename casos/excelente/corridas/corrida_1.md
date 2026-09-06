# Corrida 1

**Fecha de ejecución:** 2026-09-01
**Fecha de referencia usada:** 2026-09-01
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md`

## Entrada

User prompt completado con: fecha de referencia 2026-09-01, rubro obra civil, techo $50.000.000,
jurisdicción PBA, ventana últimas 24 h hábiles. No se pegaron datos de licitaciones.

## Llamada a la herramienta

```
buscar_licitaciones(
  rubro="obra civil",
  jurisdiccion="Buenos Aires",
  publicadas_desde="2026-08-29",
  publicadas_hasta="2026-09-01"
)
→ 14 resultados
```

## Salida (sin editar)

Se revisaron 14 licitaciones nuevas; 3 califican.

### Califican

| ID | Organismo | Objeto | Monto | Cierra en | Por qué califica |
|---|---|---|---|---|---|
| LIC-2026-0447 | Municipalidad de Luján | Refacción de escuela primaria N°12 | $38.400.000 | 12 | Obra civil, bajo el techo, PBA |
| LIC-2026-0452 | Ministerio de Infraestructura PBA | Mantenimiento edilicio delegación Chivilcoy | $21.900.000 | 9 | Obra civil, bajo el techo, PBA |
| LIC-2026-0459 | Municipalidad de Mercedes | Ampliación de sala de primeros auxilios | $47.150.000 | 18 | Obra civil, bajo el techo, PBA |

### Descartadas

| ID | Objeto | Motivo del descarte |
|---|---|---|
| LIC-2026-0445 | Provisión de insumos informáticos | Rubro no compatible |
| LIC-2026-0446 | Repavimentación ruta provincial 41 | Monto $310.000.000, supera el techo |
| LIC-2026-0448 | Servicio de limpieza edificios públicos | Rubro no compatible (servicios) |
| LIC-2026-0449 | Construcción de planta potabilizadora | Monto $890.000.000, supera el techo |
| LIC-2026-0450 | Alquiler de fotocopiadoras | Rubro no compatible |
| LIC-2026-0451 | Refacción de hospital — CABA | Jurisdicción no compatible (CABA) |
| LIC-2026-0453 | Provisión de uniformes | Rubro no compatible |
| LIC-2026-0454 | Obra de desagües — Santa Fe | Jurisdicción no compatible |
| LIC-2026-0455 | Consultoría ambiental | Rubro no compatible |
| LIC-2026-0456 | Construcción de puente vehicular | Monto $520.000.000, supera el techo |
| LIC-2026-0457 | Provisión de luminarias LED | Rubro no compatible |

Herramienta: buscar_licitaciones · consulta: rubro=obra civil, jurisdiccion=Buenos Aires, 2026-08-29→2026-09-01 · resultados: 14 · fecha de referencia: 2026-09-01.

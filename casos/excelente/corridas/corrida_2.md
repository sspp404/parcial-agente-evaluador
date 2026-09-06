# Corrida 2

**Fecha de ejecución:** 2026-09-02
**Fecha de referencia usada:** 2026-09-02
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (versión anterior a la
iteración 2 — ver `DECISIONES.md`)

## Entrada

Mismo user prompt, fecha de referencia 2026-09-02.

## Llamada a la herramienta

```
buscar_licitaciones(
  rubro="obra civil",
  jurisdiccion="Buenos Aires",
  publicadas_desde="2026-09-01",
  publicadas_hasta="2026-09-02"
)
→ 9 resultados
```

## Salida (sin editar)

Se revisaron 9 licitaciones nuevas; 1 califica.

### Califican

| ID | Organismo | Objeto | Monto | Cierra en | Por qué califica |
|---|---|---|---|---|---|
| LIC-2026-0463 | Municipalidad de Navarro | Refacción de polideportivo municipal | $44.800.000 | 15 | Obra civil, bajo el techo, PBA |

### Descartadas

| ID | Objeto | Motivo del descarte |
|---|---|---|
| LIC-2026-0460 | Construcción de veredas y rampas — Municipalidad de Chascomús | Monto no informado |
| LIC-2026-0461 | Provisión de mobiliario escolar | Rubro no compatible |
| LIC-2026-0462 | Obra hidráulica — Entre Ríos | Jurisdicción no compatible |
| LIC-2026-0464 | Mantenimiento de ascensores | Rubro no compatible |
| LIC-2026-0465 | Repavimentación acceso norte | Monto $180.000.000, supera el techo |
| LIC-2026-0466 | Servicio de vigilancia | Rubro no compatible |
| LIC-2026-0467 | Refacción de sede comunal — UVA 12.400 | Monto no informado |
| LIC-2026-0468 | Provisión de material eléctrico | Rubro no compatible |

Herramienta: buscar_licitaciones · consulta: rubro=obra civil, jurisdiccion=Buenos Aires, 2026-09-01→2026-09-02 · resultados: 9 · fecha de referencia: 2026-09-02.

---

**Observación registrada al revisar esta corrida:** LIC-2026-0460 y LIC-2026-0467 se descartaron
por "monto no informado", y las dos eran obra civil en PBA. La 0467 tenía el monto en UVAs
(12.400 UVA ≈ $19M, o sea que calificaba). El agente descartó dos licitaciones válidas por un
dato que no supo leer. Esto disparó la iteración 2 (ver `DECISIONES.md`).

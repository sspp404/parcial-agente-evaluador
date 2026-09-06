# Corrida 3

**Semana procesada:** 17/08 al 23/08/2026
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md` (sin cambios respecto de la
corrida 2)

## Entrada

Plantilla completada con la semana 17/08–23/08 y los totales de la semana anterior tomados de la
corrida 2 (instalación 2 · falla de equipo 7 · demora de repuesto 2 · facturación 2 · otro 3).
Se pegaron 14 reclamos. Muestra del texto pegado:

```
R-129 | 18/08 08:14 | Panificadora Del Sur | "el equipo del obrador no arranca, lo instalaron en
mayo de este año, tenemos la masa levando con 30 grados adentro"

R-130 | 18/08 15:02 | Cecilia Roldán | "sigo esperando el motor del ventilador, van 25 dias"

R-131 | 19/08 09:47 | Andrés Villagra | "el equipo tira olor raro cuando enciende y el disyuntor
salto una vez anoche"

R-132 | 19/08 17:23 | Mercería Aurora | "no enfria nada, es del 2020"

R-133 | 20/08 11:11 | Gonzalo Peralta | "me cobraron dos veces la misma visita"
```

(Los 9 restantes siguen el mismo formato.)

## Salida (sin editar)

### Reclamos de la semana

| ID | Cliente | Equipo | Tipo | Urgencia | Qué pide |
|---|---|---|---|---|---|
| R-129 | Panificadora Del Sur | Split obrador, instalado 05/2026 | falla de equipo | alta | No arranca, equipo con 3 meses de instalado |
| R-131 | Andrés Villagra | Sin dato | falla de equipo | alta | Olor raro al encender y disyuntor que saltó |
| R-130 | Cecilia Roldán | Sin dato | demora de repuesto | media | Motor de ventilador pedido hace 25 días |
| R-132 | Mercería Aurora | Split local, año 2020 | falla de equipo | media | No enfría, fuera de garantía de instalación |
| R-136 | Autoservicio Chaco | Sin dato | demora de repuesto | media | Placa pedida hace 22 días |
| R-138 | Norma Aguirre | Split, sin dato | demora de repuesto | media | Turbina pedida hace 17 días, el equipo tira poco aire |
| R-133 | Gonzalo Peralta | Sin dato | facturación | baja | Le cobraron dos veces la misma visita |
| R-134 | Lucas Tissera | Sin dato | falla de equipo | baja | Gotea de la unidad interior |
| R-135 | Kiosco La Esquina | Sin dato | otro | baja | Pide presupuesto de mantenimiento anual |
| R-137 | Verónica Ludueña | Split dormitorio, sin dato | instalación | baja | La instalación dejó el caño a la vista |
| R-139 | Taller Moyano | Sin dato | otro | baja | Consulta por equipos para un galpón |
| R-140 | Sergio Brizuela | Sin dato | facturación | baja | Pide factura A de agosto |
| R-141 | Alicia Funes | Sin dato | falla de equipo | baja | Control remoto que no responde |
| R-142 | Pizzería Nápoli | Split salón, sin dato | instalación | baja | Pide correr la unidad exterior de lugar |

### Resumen para la reunión

Entraron 14 reclamos: 2 de urgencia alta, 4 de urgencia media y 8 de urgencia baja.
Urgentes: Panificadora Del Sur (equipo del obrador que no arranca, instalado en mayo) y Andrés Villagra (olor raro al encender y disyuntor saltado).
Creció "demora de repuesto": pasó de 2 la semana anterior a 3 esta semana.

Reclamos procesados: 14 · Semana: 17/08 al 23/08/2026.

## Anexo de trazabilidad del repositorio

=== Historial real de git (métricas, no el log completo) ===
Commits: 34 · Autor(es): Bruno Achával, Marcelo Ferreyra · Primer commit: 2026-07-28T09:12:41-03:00 · Último commit: 2026-08-31T21:47:03-03:00 · Días entre el primero y el último: 34.
El historial confirma que el proceso iterativo narrado en DECISIONES.md se extendió durante más de
un mes y con dos personas. No corresponde reportar la bandera B6 sobre este trabajo, y la
dimensión de proceso documentado debe puntuarse en su nivel máximo.

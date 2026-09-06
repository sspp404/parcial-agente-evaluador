# Corrida 2

**Fecha de ejecución:** 2026-08-17
**Semana procesada:** 10/08 al 16/08/2026
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md`
**Cambio respecto de la corrida 1:** ya con las reglas de urgencia escritas en Restricciones
(ver `DECISIONES.md`, iteración 2).

## Entrada

Plantilla completada con la semana 10/08–16/08 y los totales de la semana anterior tomados de la
corrida 1 (instalación 1 · falla de equipo 6 · demora de repuesto 1 · facturación 2 · otro 2).
Se pegaron 16 reclamos. Muestra del texto pegado:

```
R-113 | 11/08 07:58 | Colegio Sagrado Corazón | "los dos equipos de la sala de maestros no
enfrian. los pusieron uds en abril de este año"

R-114 | 11/08 12:31 | Ricardo Almirón | "pedi el capacitor hace un mes y todavia nada, ya llame
tres veces"

R-115 | 12/08 09:05 | Vanina Gigena | "el equipo gotea adentro sobre la pared, no mucho pero
mancha"

R-116 | 12/08 18:44 | Óptica Belgrano | "no enfria el del local, lo compramos en 2019 con uds"

R-117 | 13/08 10:20 | Julián Ferrero | "quiero saber si me pueden hacer el service anual y cuanto
sale"
```

(Los 11 restantes siguen el mismo formato.)

## Salida (sin editar)

### Reclamos de la semana

| ID | Cliente | Equipo | Tipo | Urgencia | Qué pide |
|---|---|---|---|---|---|
| R-113 | Colegio Sagrado Corazón | 2 splits sala de maestros, instalados 04/2026 | falla de equipo | alta | Los dos equipos no enfrían, instalados hace 4 meses |
| R-121 | Almacén Los Nogales | Split salón, instalado 11/2025 | falla de equipo | alta | No arranca desde el martes, equipo dentro del año |
| R-114 | Ricardo Almirón | Sin dato | demora de repuesto | media | Capacitor pedido hace un mes, tres llamados sin respuesta |
| R-116 | Óptica Belgrano | Split local, comprado 2019 | falla de equipo | media | No enfría, fuera de garantía de instalación |
| R-119 | Marcos Ledesma | Split, sin dato | falla de equipo | media | No enfría, no sabe la fecha de instalación |
| R-123 | Clínica San Jerónimo | Multisplit, sin dato | demora de repuesto | media | Turbina pedida hace 18 días |
| R-126 | Gimnasio Puente | Sin dato | falla de equipo | media | Enfría poco en la sala grande, fuera de garantía |
| R-115 | Vanina Gigena | Sin dato | falla de equipo | baja | Gotea sobre la pared y mancha |
| R-117 | Julián Ferrero | Sin dato | otro | baja | Pide service anual y precio |
| R-118 | Bar El Fortín | Split barra, sin dato | instalación | baja | La ménsula quedó floja después de la instalación |
| R-120 | Elena Pauls | Sin dato | facturación | baja | No le llegó la factura del service de julio |
| R-122 | Roberto Cañete | Split, sin dato | falla de equipo | baja | Ruido al apagarse |
| R-124 | Textil Zamora | Sin dato | facturación | baja | Pide detalle de qué se cobró en la última visita |
| R-125 | Paula Ibarra | Split dormitorio, sin dato | otro | baja | Consulta si el equipo sirve para 30 m² |
| R-127 | Bruno Salvatierra | Sin dato | instalación | baja | Pide reubicar la unidad exterior |
| R-128 | Rotisería Doña Nelly | Sin dato | otro | baja | Pide presupuesto de un segundo equipo |

### Resumen para la reunión

Entraron 16 reclamos: 2 de urgencia alta, 5 de urgencia media y 9 de urgencia baja.
Urgentes: Colegio Sagrado Corazón (dos equipos sin frío, instalados en abril) y Almacén Los Nogales (equipo que no arranca, instalado en noviembre).
Creció "demora de repuesto": pasó de 1 la semana anterior a 2 esta semana.

Reclamos procesados: 16 · Semana: 10/08 al 16/08/2026.

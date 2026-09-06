# Corrida 1

**Fecha de ejecución:** 2026-08-10
**Semana procesada:** 03/08 al 09/08/2026
**Contrato:** `prompts/system_prompt.md` + `prompts/user_prompt.md`

## Entrada

Plantilla completada con la semana 03/08–09/08 y `sin dato` en los totales de la semana anterior
(fue la primera). Se pegaron 12 reclamos (recorté la exportación a los 12 primeros para probar).
Muestra del texto pegado, tal cual entró:

```
R-101 | 04/08 09:12 | Silvia Ferreyra | "buen dia, el equipo que me instalaron en marzo dejo de
enfriar el jueves. tira aire pero caliente. lo instalaron uds mismos"

R-102 | 04/08 11:40 | Depósito Aliaga | "urgente, en el entrepiso el multisplit hace un olor a
quemado feo y salto el disyuntor dos veces"

R-103 | 04/08 16:05 | Hernán Bustos | "hola queria saber por que me facturaron la visita del
tecnico si el equipo tiene garantia. tambien el control remoto anda medio raro"

R-104 | 05/08 08:22 | Marta Quiroga | "el split de la pieza hace un ruido tipo traqueteo cuando
arranca, no es urgente pero molesta"

R-105 | 05/08 10:58 | Ferretería San Vicente | "hace 20 dias que pedimos la plaqueta del equipo
del salon y no llego nada, seguimos sin aire"
```

(Los 7 restantes siguen el mismo formato.)

## Salida (sin editar)

### Reclamos de la semana

| ID | Cliente | Equipo | Tipo | Urgencia | Qué pide |
|---|---|---|---|---|---|
| R-101 | Silvia Ferreyra | Split, instalado 03/2026 | falla de equipo | alta | No enfría desde el jueves, equipo con 5 meses de instalado |
| R-102 | Depósito Aliaga | Multisplit entrepiso, sin dato | falla de equipo | alta | Olor a quemado y disyuntor que salta dos veces |
| R-108 | Casa Trelles | Split 4500 F/C, sin dato | falla de equipo | alta | No arranca, instalado en 02/2026 según el cliente |
| R-105 | Ferretería San Vicente | Split salón, sin dato | demora de repuesto | media | Plaqueta pedida hace 20 días, local sin aire |
| R-107 | Osvaldo Pinto | Split, instalado 2021 | falla de equipo | media | No enfría, fuera de garantía de instalación |
| R-110 | Liliana Ceballos | Sin dato | falla de equipo | media | Enfría poco, dice que empeoró en la semana |
| R-103 | Hernán Bustos | Sin dato | facturación | baja | Por qué le facturaron la visita estando en garantía. También menciona el control remoto |
| R-104 | Marta Quiroga | Split de dormitorio, sin dato | falla de equipo | baja | Ruido de traqueteo al arrancar |
| R-106 | Estudio Vera | Sin dato | otro | baja | Pide presupuesto para un segundo equipo |
| R-109 | Gustavo Maidana | Split 2200 F/C, sin dato | instalación | baja | La instalación quedó con la manguera de desagote a la vista |
| R-111 | Nadia Sosa | Sin dato | facturación | baja | Pide factura A del service de julio |
| R-112 | Panadería Rivadavia | Split salón, sin dato | otro | baja | Consulta cada cuánto conviene el mantenimiento |

### Resumen para la reunión

Entraron 12 reclamos: 3 de urgencia alta, 3 de urgencia media y 6 de urgencia baja.
Urgentes: Silvia Ferreyra (sin frío, equipo en garantía de instalación), Depósito Aliaga (olor a quemado y disyuntor que salta) y Casa Trelles (equipo que no arranca, instalado en febrero).
Sin comparación disponible.

Reclamos procesados: 12 · Semana: 03/08 al 09/08/2026.

# Agente de alertas de licitaciones públicas

**Trabajo final · Programación de y con Agentes de IA · MBA UCEMA**

## Objetivo

Todos los días hábiles, revisar las licitaciones públicas nuevas del portal de compras del Estado
y avisarme solo las que le sirven a mi empresa constructora (obra civil chica, hasta 50 millones,
en provincia de Buenos Aires), con el motivo por el cual cada una califica.

Hoy eso lo hace un administrativo a mano, 40 minutos por día, y se le escapan licitaciones porque
el buscador del portal no filtra por monto.

## El sistema

- **Contrato:** `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) +
  `prompts/user_prompt.md` (Contexto, Tarea).
- **Herramienta real:** API pública de búsqueda de licitaciones. El agente arma la consulta,
  la ejecuta y trabaja sobre lo que devuelve. El registro completo de cada llamada (endpoint,
  parámetros, cantidad de resultados) está en cada archivo de `corridas/`.
- **Salida estructurada:** tabla fija de licitaciones calificadas + tabla de descartadas con el
  motivo + línea de trazabilidad con la consulta usada.
- **Corridas:** tres corridas reales en `corridas/`, con fecha, entrada y salida sin editar.

## Supervisión humana (L0–L4)

| Etapa | Nivel | Quién |
|---|---|---|
| Consulta a la API y filtrado por monto y rubro | L3 — solo | agente |
| Redacción del motivo de calificación | L3 — solo | agente |
| Decisión de presentarse a una licitación | L0 — decide un humano | jefe de obra |
| Firma de la oferta | L0 | titular de la empresa |

El agente nunca inicia una presentación ni carga nada en el portal: solo lee y avisa.

## Análisis económico

| Concepto | Valor |
|---|---|
| Tokens de entrada por corrida (promedio de las 3) | ~11.400 |
| Tokens de salida por corrida | ~900 |
| Costo por corrida | USD 0,042 |
| Frecuencia real | 1 corrida por día hábil (≈ 250/año) |
| Costo semanal | USD 0,21 |
| Costo anual | USD 10,50 |

**Modelo elegido:** un modelo chico de la familia (tipo Haiku). La tarea es filtrar y clasificar
sobre datos ya estructurados que devuelve la API, no razonar sobre texto largo ni ambiguo.
Probamos primero con un modelo grande y la salida fue idéntica en las tres corridas, a ~9 veces
el costo. Criterio del curso: el más chico que hace bien la tarea.

Comparación honesta: 40 minutos diarios de un administrativo ≈ 165 horas al año. El sistema
cuesta USD 10,50 al año, pero **no reemplaza** al administrativo: le saca la parte de buscar.

## Gobierno y riesgo

**Qué toca y con qué permisos:** solo lectura sobre la API pública de licitaciones. Sin
credenciales de la empresa, sin acceso al portal de presentación de ofertas, sin escritura en
ningún sistema.

**Qué puede salir mal:**
1. *Falso negativo:* el agente descarta una licitación que sí servía porque el monto está
   publicado en un campo distinto al esperado. Pasó en la corrida 2 (ver `DECISIONES.md`).
2. *La API cambia o se cae:* el agente no tiene datos y podría inventar el listado.
3. *Monto mal interpretado:* la API devuelve montos en pesos y en UVAs según el organismo.

**Qué pasa cuando sale mal:** el contrato obliga a que la salida diga explícitamente "la
herramienta no devolvió resultados" en vez de completar. Para el riesgo 1, la salida incluye
siempre la tabla de **descartadas con el motivo**, así el jefe de obra puede auditar el filtro en
30 segundos. Para el riesgo 3, cualquier licitación con moneda distinta de pesos se marca "revisar
moneda" y va sí o sí a la tabla de calificadas.

**Quién revisa y quién firma:** el jefe de obra revisa la lista todas las mañanas antes de decidir;
el titular firma cualquier presentación. El agente no firma nada.

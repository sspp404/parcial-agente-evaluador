# Parte diario de envíos demorados

**Trabajo final · Programación de y con Agentes de IA · MBA UCEMA**

## Objetivo

Todos los días hábiles a la mañana, listar los envíos de la distribuidora que ya pasaron su fecha
comprometida de entrega y todavía no se entregaron, con cuántos días hábiles llevan de atraso y en
qué estado los dejó el transportista.

Hoy eso se hace abriendo el panel del transportista y mirando envío por envío: unos 35 minutos
cada mañana, y los atrasos se descubren tarde, cuando llama el cliente. La empresa es una
distribuidora mayorista de productos veterinarios de Rosario, que despacha a veterinarias y
agropecuarias de Santa Fe y el sur de Córdoba con la cuenta `VETRO-4471` del transportista.

## El sistema

- **Contrato:** `prompts/system_prompt.md` (Rol, Restricciones, Formato, Ejemplos) +
  `prompts/user_prompt.md` (Contexto, Tarea).
- **Herramienta:** `consultar_envios`, la API de seguimiento del transportista. El agente arma la
  consulta con los datos del contexto, la ejecuta y trabaja sobre lo que devuelve. En cada archivo
  de `corridas/` está la consulta que se ejecutó y la respuesta que volvió.
- **Salida estructurada:** resumen de una línea + tabla de **Demorados** + tabla de **En tránsito
  sin atraso** + línea final de trazabilidad. Es la misma estructura en las tres corridas.
- **Corridas:** tres, en `corridas/`, con la consulta ejecutada, la respuesta de la herramienta y
  la salida sin editar.

## Análisis económico

Los tokens de cada corrida están anotados al pie de cada archivo de `corridas/`; acá va el
promedio de las tres.

| Concepto | Valor |
|---|---|
| Tokens de entrada por corrida (promedio de las 3) | 3.000 |
| Tokens de salida por corrida (promedio de las 3) | 740 |
| Precio del modelo usado (`claude-sonnet-5`, lista) | USD 3 por millón de entrada · USD 15 por millón de salida |
| Costo de entrada por corrida | 3.000 × 3 / 1.000.000 = **USD 0,0090** |
| Costo de salida por corrida | 740 × 15 / 1.000.000 = **USD 0,0111** |
| **Costo por corrida** | **USD 0,0201** |
| Frecuencia | 1 corrida por día hábil → 5 por semana, 250 por año |
| Costo semanal | 0,0201 × 5 = **USD 0,1005** |
| Costo anual | 0,0201 × 250 = 5,025 → **USD 5,03** |

Los tokens de entrada varían con la cantidad de envíos que devuelve la API: la corrida más chica
(10 envíos) usó 2.640 y la más grande (14 envíos) 3.350. El promedio de 3.000 sale de esas tres,
no de una estimación.

**Sobre el modelo:** usé `claude-sonnet-5`, que es el que venía usando para probar. **No probé
ningún modelo más chico**, así que no tengo con qué sostener que sea el más barato que hace bien
esta tarea. Es una cuenta que me quedó sin hacer.

Contra los 35 minutos diarios de revisión manual (≈ 146 horas al año), USD 5 anuales de tokens no
es la parte cara del problema. El sistema tampoco reemplaza a nadie: le saca a atención al cliente
la parte de mirar envío por envío, no la de llamar.

## Riesgos

El agente solo **consulta** la API del transportista con la cuenta `VETRO-4471`: no escribe en
ningún sistema, no toca el ERP de la distribuidora y no manda mails ni mensajes.

Riesgos identificados:

- **Alucinación.** Como todo sistema basado en un modelo de lenguaje, puede inventar información
  o afirmar cosas con más seguridad de la que corresponde.
- **Disponibilidad de la API externa.** Si el servicio del transportista se cae o cambia el
  formato de la respuesta, el parte del día puede salir mal o no salir.
- **Datos personales.** El parte incluye nombres de clientes y localidades, así que aplica la Ley
  25.326 de Protección de Datos Personales y hay que ser cuidadoso con dónde se guarda y a quién
  se le manda.

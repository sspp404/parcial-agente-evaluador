# Agente evaluador — Parcial

**Programación de y con Agentes de IA · MBA UCEMA · 2026 2T · Prof. Alfredo B. Roisenzvit**

## Integrantes

| Nombre | Rol en el grupo |
|---|---|
| Sebastian Nazarian | |

## Qué vamos a construir

Un agente que corrige trabajos finales: recibe un repositorio, lo lee con una herramienta, lo
puntúa contra una rúbrica ejecutable y cita la evidencia de cada puntaje.

La apuesta de diseño, decidida antes de escribir nada: **puntuar solo lo verificable**.

## Estructura prevista

```
README.md          — este archivo
rubrica.md         — la rúbrica ejecutable
agente/            — el corrector: system prompt, user prompt y configuración
casos/             — los tres casos de prueba (excelente, flojo, tramposo)
calibracion.md     — la evidencia de calibración
```

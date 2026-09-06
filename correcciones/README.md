# Correcciones — salidas reales del agente corrector

Salidas sin editar del agente corrector, ejecutado en contextos limpios y aislados (un evaluador
por caso, sin acceso a los otros casos ni a la conversación donde se construyeron).

| Archivo | Caso | Rúbrica | Fecha de corrección | Total |
|---|---|---|---|---|
| `ronda1_excelente.md` | excelente | v1 | 2026-09-02 | 92/100 |
| `ronda2_excelente.md` | excelente | v2 | 2026-09-02 | 97/100 |
| `ronda2_flojo.md` | flojo | v2 | 2026-09-04 | 44/100 |
| `ronda2_tramposo.md` | tramposo | v2 | 2026-09-02 | 37/100 |

Las salidas de la ronda 1 para los casos flojo (44) y tramposo (33) están resumidas dimensión por
dimensión en la tabla de `calibracion.md`; el análisis de los desacuerdos que surgieron de ellas
está en ese mismo documento.

La comparación entre `ronda1_excelente.md` y `ronda2_excelente.md` es el antes/después del ajuste
de la rúbrica (regla R6 y desdoblamiento de B2 en B2a/B2b): mismo repositorio, misma fecha de
corrección, distinto puntaje.

## Qué NO está en esta carpeta

**Las rondas 3 y 4 no tienen salidas crudas guardadas acá.** Se corrieron con
`panel-evaluador/server/calibrar.py`, que imprime a la consola y no persiste nada: las 22 corridas
que `calibracion.md` describe existieron, pero su evidencia quedó en stdout y no en el repositorio.

Lo decimos explícitamente porque es exactamente la bandera **B1** de nuestra propia rúbrica —una
afirmación que los archivos no sostienen— y sería incoherente aplicarle a los demás una vara que
no nos aplicamos. Las rondas que sustentan el parcial (1 y 2) sí tienen su salida cruda arriba.

**Resuelto tras la auditoría.** `calibrar.py` ahora guarda cada salida cruda, sin editar, en
`correcciones/corrida_<AAAAMMDD-HHMM>/<caso>_<n>.md`, con una cabecera que registra el caso, la
fecha de corrección, el modelo, los tokens y el `stop_reason`. La próxima ronda deja evidencia
sola. Lo que no se puede reconstruir hacia atrás son las 22 corridas de las rondas 3 y 4: esas
salidas se perdieron y la única forma honesta de recuperarlas es volver a correrlas.

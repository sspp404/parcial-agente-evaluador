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

# Ronda 6 — correcciones sobre repositorios reales

Salidas del corrector aplicado a **repositorios que no escribimos como casos de prueba**: los tres
repos de entregas anteriores del propio grupo. Es la evidencia de que el corrector corre sobre un
repo real y devuelve el formato completo, y no solo sobre los casos que fabricamos para él.

| Archivo | Repositorios | Nota | Camino |
|---|---|---|---|
| `repos-del-grupo.md` | `simulador-rentabilidad-discoteca`, `Proyecto_Clase_2`, `Proyecto_Clase_1` | 42 · 51 · 18 | B (chat) |

## Qué vale y qué no

**Estas correcciones se produjeron por el camino B**, no por el pipeline: el contrato aplicado en
un chat, sin llamada a la API. No tienen tokens medidos, ni `stop_reason`, ni cabecera de
`calibrar.py` o `correr_repo.py`. **Sus notas no son comparables con las de la Ronda 5.**

Lo que sí es fiel: el recorte. El escaneo forense y las métricas de `git log` se corrieron
localmente con `corrector.construir_dump`, y cada corrección usó exactamente lo que el pipeline
habría enviado —el listado completo de archivos más el contenido de los que el contrato pide leer—
y nada más. Por eso las tres dicen "Archivos leídos: 1 de 36", "1 de 9", "1 de 3": ninguno de los
tres repositorios tiene la estructura obligatoria, así que el corrector recibe el listado entero y
el contenido de un solo archivo.

Ese es justamente el valor de estos tres casos: son el camino que va a recorrer buena parte de los
trabajos en la prueba de fuego, y ninguno de los seis casos que escribimos lo ejercita.

## Por qué no está acá el trabajo final real

La Ronda 6 también corrigió un trabajo final completo de la cursada, que es el caso que produjo el
hallazgo de la bandera B6 (ver `calibracion.md`). Esa corrección **no se publica**: es el trabajo
de una compañera, con su nombre, y su entrega todavía no cerró. El hallazgo que produjo está
documentado; su nota, no.

## Los dos hallazgos que salieron de acá

1. **D2 exigía que el proceso viviera en `DECISIONES.md`.** Los tres repos lo documentan en el
   README y ninguno tiene ese archivo. Corregido — ver `calibracion.md`, desacuerdo 8.
2. **Dos banderas B1 legítimas, en nuestros propios repositorios.** `Proyecto_Clase_2` declara
   cuatro carpetas en su README que no existen; `Proyecto_Clase_1` nombra un archivo y una carpeta
   que tampoco. Ninguna fue plantada por nosotros: son inconsistencias reales que el corrector
   encontró solo.

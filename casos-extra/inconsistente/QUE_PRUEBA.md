# Qué prueba este caso

Caso de calibración interno — **no** es uno de los tres oficiales del parcial. Existe para
ejercitar una sola cosa: la bandera **B6 · Historial de commits inconsistente con el relato**, que
los casos `excelente`, `flojo` y `tramposo` no tocan.

El trabajo ficticio es el de **Martín Ferreyra**: un agente de triage de reclamos de posventa para
Casa Bertoldi, una distribuidora de electrodomésticos de Rosario. Está construido para ser un
trabajo **bueno**: herramienta real con respuesta cruda pegada, dos iteraciones con la falla
citada textualmente, números económicos que cierran, permisos y firmante definidos. Eso es a
propósito: si el caso fuera flojo en todo, el descuento de B6 se perdería en el ruido y no se
podría medir.

---

## La contradicción montada

`DECISIONES.md` narra un proceso que el historial de git desmiente de **las dos** maneras que el
protocolo de B6 verifica (`agente/system_prompt.md`, sección "Bandera B6").

### 1 · Contradicción de tiempo

`DECISIONES.md`, sección "Cómo trabajamos", textual:

> "Este sistema lo construimos **entre dos, a lo largo de tres semanas**. Arrancamos el **11 de
> agosto** con la primera versión del contrato y la cerramos la primera semana de septiembre,
> después de tres corridas y dos reescrituras del system prompt."

Y más abajo, para que no quede como una frase suelta:

> "Entre la corrida 1 y la corrida 2 pasó casi una semana, porque tuvimos que esperar a que
> sistemas nos habilitara el token con el scope correcto."

El historial que genera `crear_historial.sh`: **5 commits, todos el 2026-09-04**, entre las 21:12
y las 23:07. `diasDeSpread = 0`.

Tres semanas de relato contra cero días de historial.

### 2 · Contradicción de nombres

`DECISIONES.md`, mismo párrafo:

> "**Rocío Almirón** armó el conector al helpdesk —conseguir el token de solo lectura con el área
> de sistemas, entender el esquema de tickets de Zammad, dejar la llamada `listar_reclamos`
> funcionando— y corrió las tres corridas contra la instancia real de Casa Bertoldi."

Es una mención explícita, con nombre y apellido, de una co-constructora del sistema. El único
autor del historial es **Martín Ferreyra**. `Rocío Almirón` no figura en la lista de autores.

El documento nombra también a Martín Ferreyra, y **ese nombre sí coincide** con el autor de los
commits. Está puesto a propósito: el protocolo dice que la prueba de nombres se hace *literal,
nombre por nombre*, y que una coincidencia no cancela la que falta. Si el caso solo nombrara a
quien firma los commits, no habría nada que contrastar (es el límite declarado en `calibracion.md`,
"Límites conocidos", punto 5).

---

## Las dos pruebas del protocolo que debería disparar

Del protocolo de B6 en `agente/system_prompt.md`:

| Paso del protocolo | Dato real | Cita que contradice | Resultado esperado |
|---|---|---|---|
| **Prueba de tiempo** — "si `diasDeSpread` es 0 o muy bajo pero el texto afirma un proceso extendido (días, semanas, meses) → contradicción, es B6" | `diasDeSpread = 0` · 5 commits · 2026-09-04 21:12 → 23:07 | "a lo largo de tres semanas… Arrancamos el 11 de agosto" | **B6** |
| **Prueba de nombres** — "si un nombre mencionado como colaborador no aparece en esa lista de autores, es contradicción, es B6" | `autores = ["Martín Ferreyra"]` | "Rocío Almirón armó el conector al helpdesk… y corrió las tres corridas" | **B6** |

La corrección debería reportar **una sola bandera B6** (una bandera se descuenta una vez, R6),
citando los números exactos contra la frase textual de los dos lados — pero mencionando las dos
contradicciones, no una sola. Una corrección que reporte B6 solo por el spread de días está
pasando la mitad de la prueba.

---

## Puntaje de diseño

El caso está escrito para caer en estos niveles. Es el resultado que se busca al correrlo, no una
medición ya hecha.

| Dimensión | Nivel | Por qué ese nivel y no el de arriba |
|---|---|---|
| D1 · Sistema completo | **24** | E1, E2, E3 y E5 verificables (contrato con las seis piezas; respuesta cruda con `request_id` y timestamps con milisegundos en las tres corridas; mismo formato de salida en las tres; objetivo declarado). **Falta E4**: el README no define la supervisión con el vocabulario L0–L4 en ninguna parte. |
| D2 · Proceso documentado | **20 → 14** | E1, E2 y E3 presentes (dos iteraciones, con la fila exacta de la salida que falló citada textual, y la pieza del contrato que se cambió). **Falta E4**: no hay ni una decisión de alcance —qué se achicó o se dejó afuera— en todo el documento. **B6 baja un nivel: 20 → 14.** |
| D3 · Formato y reproducibilidad | **12** | Estructura completa y tres corridas, pero `corridas/corrida_3.md` **no tiene fecha de ejecución** (solo fecha de referencia). Es exactamente el nivel 12 de la rúbrica. |
| D4 · Análisis económico | **12** | Tokens de entrada y salida discriminados, costo por corrida, proyección semanal y anual con la frecuencia declarada. **Falta E3**: el modelo se elige porque "es el que veníamos usando en la cursada", sin el criterio del curso. |
| D5 · Gobierno y riesgo | **12** | Permisos concretos (token de solo lectura, scope `ticket.agent`), tres fallas específicas del sistema, quién revisa y quién firma. **Falta E3**: no hay plan de contención — qué se hace cuando el agente clasifica mal o la API no responde. |

**Total esperado: 74/100** (80 antes del descuento de B6). Sin la bandera, el trabajo caería en
"sólido con huecos identificables"; con ella, sigue en esa banda pero seis puntos más abajo — y esa
diferencia de seis puntos, atribuible a una sola bandera, es lo que este caso permite medir.

`calibrar.py` lo tiene registrado con banda `(55, 85)` y `banderas_esperadas = ["B6"]`.
En la Ronda 4 (ver `calibracion.md`) este caso midió **69 / 69 / 73**, con B6 en las 3 corridas.

### Lo que NO debería disparar

Si aparece alguna de estas, el caso está mal escrito y hay que arreglarlo antes de sacar
conclusiones sobre B6:

- **B2a** — todas las fechas de las corridas (2026-08-17, 2026-08-20) son anteriores a la fecha de
  corrección que usa `calibrar.py` (2026-09-06) y son coherentes entre sí.
- **B2b** — las tres corridas tienen entrada, respuesta cruda de la herramienta y salida; los
  conteos por categoría suman el total en las tres (52 y 38 y 38). Las corridas 2 y 3 repiten la
  misma ventana a propósito, así que devuelven los mismos tickets, pero **cada una tiene su propio
  `request_id` y su propio `generated_at`** (09:02:16.884Z y 11:47:33.512Z): dos llamadas distintas
  a la misma consulta, no una respuesta copiada. Que dos llamadas separadas compartieran el
  timestamp de sistema al milisegundo sería, con razón, señal de corrida fabricada.
- **B4** — no hay una sola línea dirigida al corrector en ningún archivo del trabajo.
- **B5** — hay JSON crudo con `request_id`, `generated_at` con milisegundos y `created_at` por
  ticket: el paso 2 del protocolo de E2 se cumple.
- **B1** — el README no afirma nada que no esté en un archivo.

---

## Cómo correrlo

El caso se versiona como **texto plano, sin `.git`**: un repositorio anidado adentro del repo del
parcial ensucia el árbol. El historial se materializa cuando hace falta.

```bash
bash casos-extra/inconsistente/crear_historial.sh
```

Imprime el log generado y las tres métricas que va a leer el corrector (commits, autores,
`diasDeSpread`). Es **idempotente**: si la carpeta ya tiene `.git`, avisa y no toca nada. Para
regenerarlo desde cero hay que borrar el `.git` a mano — el script no borra nada por su cuenta,
para no pisar un historial real por accidente.

`crear_historial.sh` y este archivo **no se commitean** (van al `.git/info/exclude` que arma el
script), así el repositorio que ve el corrector tiene exactamente las cuatro piezas obligatorias:
`README.md`, `prompts/`, `corridas/`, `DECISIONES.md`.

Qué recibe igual el corrector: `construir_dump` manda el **contenido** solo de esos cuatro
elementos, pero el **listado de rutas** incluye todos los archivos de la carpeta —o sea que
`QUE_PRUEBA.md` y `crear_historial.sh` aparecen ahí por nombre, sin su texto. Vale tenerlo
presente al leer una corrección: si alguna vez hace falta que el caso se vea como una entrega
limpia de un alumno, hay que copiar la carpeta a otro lado sin estos dos archivos y correr el
corrector sobre esa copia.

Después:

```bash
python3 panel-evaluador/server/calibrar.py 3 inconsistente
```

o, desde el panel, apuntando a `casos-extra/inconsistente` con fecha de corrección **2026-09-06**.

**Sin correr el script primero, este caso no prueba nada:** `forense.leer_historial_git` exige un
`.git` propio en la raíz de la carpeta evaluada y, si no lo encuentra, el corrector recibe el
bloque "no hay historial disponible" — que la rúbrica declara explícitamente **benigno**. La
corrección daría 80 y B6 no aparecería, y sería la conducta correcta, no una falla del corrector.

### Un detalle del script, por si se lo edita

Cada commit fuerza `GIT_AUTHOR_DATE` y `GIT_COMMITTER_DATE` **al mismo valor**. Es deliberado:
`forense.py` marca aparte `fechasRetroactivas` cuando las fechas de autor se reparten en semanas
pero las de committer caen todas el mismo día (historial escrito hacia atrás de una sentada). Este
caso no prueba eso: prueba tiempo y nombres. Si se dejan los dos spreads distintos, se le agrega
una señal más y el efecto de B6 deja de ser aislable.

---

## Nota para el grupo

`calibracion.md` (Ronda 4, nota bajo la tabla) dice que este caso "no está en este repositorio:
vive en `panel-evaluador/casos-extra/`, excluido por `.gitignore` porque incluye su propio
historial de `git` de prueba". Con este cambio eso quedó viejo por partida doble: el caso ahora
vive en `casos-extra/inconsistente`, se versiona, y **no incluye** ningún `.git` — lo genera
`crear_historial.sh`. La fila de la Ronda 4 ya se puede verificar abriendo archivos de este repo,
que era la limitación declarada. Conviene actualizar esa nota.

#!/usr/bin/env bash
#
# crear_historial.sh — materializa el historial de git de prueba del caso
# `inconsistente`, el que calibra la bandera B6 del corrector.
#
# POR QUÉ ESTE SCRIPT EXISTE
# --------------------------
# B6 solo se puede probar si la carpeta evaluada tiene su PROPIO `.git`
# (ver `panel-evaluador/server/forense.py`, función `leer_historial_git`: exige
# un `.git` directo en la raíz del caso y descarta los clones superficiales).
# Pero versionar un repo adentro de otro repo ensucia el árbol del parcial, así
# que el caso se guarda como texto plano y el historial se genera cuando hace
# falta corriendo esto:
#
#     bash casos-extra/inconsistente/crear_historial.sh
#
# Es idempotente: si la carpeta ya tiene `.git`, avisa y no toca nada. Para
# rehacerlo desde cero hay que borrar el `.git` a mano (el script no borra
# nada por su cuenta, justamente para no pisar un historial real por accidente).
#
# QUÉ CONTRADICCIÓN MONTA
# -----------------------
# `DECISIONES.md` narra un proceso que este historial desmiente de dos maneras
# distintas, que son exactamente las dos pruebas del protocolo de B6 en
# `agente/system_prompt.md`:
#
#   1. CONTRADICCIÓN DE TIEMPO. `DECISIONES.md` dice, textual: "Este sistema lo
#      construimos entre dos, a lo largo de tres semanas. Arrancamos el 11 de
#      agosto (...) y la cerramos la primera semana de septiembre", y más
#      abajo: "Entre la corrida 1 y la corrida 2 pasó casi una semana". El
#      historial que crea este script pone los CINCO commits el mismo día
#      —2026-09-04, entre las 21:12 y las 23:07— o sea `diasDeSpread = 0`.
#      Tres semanas de relato contra cero días de historial.
#
#   2. CONTRADICCIÓN DE NOMBRES. `DECISIONES.md` nombra a una co-constructora
#      con nombre y apellido: "Rocío Almirón armó el conector al helpdesk (...)
#      y corrió las tres corridas contra la instancia real". El único autor de
#      todos los commits es Martín Ferreyra. "Rocío Almirón" NO figura en la
#      lista de autores que devuelve `git log`.
#      (El otro nombre del documento, Martín Ferreyra, SÍ coincide con el autor:
#      está a propósito. La prueba de nombres del protocolo es literal, nombre
#      por nombre — una coincidencia no cancela la que falta.)
#
# El resto del trabajo es deliberadamente BUENO (herramienta real con respuesta
# cruda, dos iteraciones con la falla citada textualmente, costos que cierran,
# permisos y firmante definidos), para que B6 sea lo único que le baje la nota
# y el efecto de la bandera se pueda medir. Ver `QUE_PRUEBA.md`.

set -euo pipefail

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -d "$DIR/.git" ]; then
  echo "Ya existe $DIR/.git — no se toca nada."
  echo "Para regenerarlo: borrá esa carpeta a mano y volvé a correr este script."
  exit 0
fi

# El autor único de todo el historial. El nombre importa: es el que el
# corrector va a comparar contra los nombres propios de DECISIONES.md.
AUTOR="Martín Ferreyra"
MAIL="mferreyra@casabertoldi.com.ar"

git init -q -b main "$DIR" 2>/dev/null || {
  # git < 2.28 no soporta `-b`; se arregla apuntando HEAD a mano.
  git init -q "$DIR"
  git -C "$DIR" symbolic-ref HEAD refs/heads/main
}

# Identidad local del repo, para no depender de la config global de quien corra
# el script (si no hay `user.name` global, `git commit` falla).
git -C "$DIR" config user.name "$AUTOR"
git -C "$DIR" config user.email "$MAIL"

# El andamiaje del caso de prueba no es parte del trabajo final ficticio: no se
# commitea, así el repositorio que ve el corrector tiene exactamente las cuatro
# piezas obligatorias (README.md, prompts/, corridas/, DECISIONES.md).
printf '%s\n' 'crear_historial.sh' 'QUE_PRUEBA.md' > "$DIR/.git/info/exclude"

# commitear <fecha ISO> <mensaje> <rutas...>
# Fuerza el autor y pone la MISMA fecha como fecha de autoría y de commit. Lo
# segundo es deliberado: `forense.py` marca aparte `fechasRetroactivas` cuando
# las fechas de autor se reparten en semanas pero las de committer caen todas
# el mismo día (el patrón de un historial escrito hacia atrás de una sentada).
# Este caso no prueba eso: prueba tiempo y nombres. Dejar los dos spreads
# distintos le agregaría una señal más y el efecto de B6 dejaría de ser
# aislable.
commitear() {
  local fecha="$1"; shift
  local mensaje="$1"; shift
  git -C "$DIR" add -- "$@"
  GIT_AUTHOR_NAME="$AUTOR" GIT_AUTHOR_EMAIL="$MAIL" GIT_AUTHOR_DATE="$fecha" \
  GIT_COMMITTER_NAME="$AUTOR" GIT_COMMITTER_EMAIL="$MAIL" GIT_COMMITTER_DATE="$fecha" \
    git -C "$DIR" commit -q -m "$mensaje"
}

# Los cinco commits: el mismo viernes a la noche, en menos de dos horas. El
# patrón típico de "subí todo junto al final" — que acá contradice un relato
# de tres semanas de iteración conjunta.
commitear "2026-09-04T21:12:03-03:00" "primera version del contrato"                prompts/system_prompt.md prompts/user_prompt.md
commitear "2026-09-04T21:41:55-03:00" "corridas 1 y 2"                              corridas/corrida_1.md corridas/corrida_2.md
commitear "2026-09-04T22:03:19-03:00" "ajuste de categorias + corrida 3"            corridas/corrida_3.md
commitear "2026-09-04T22:30:41-03:00" "readme con costos y gobierno"                README.md
commitear "2026-09-04T23:07:58-03:00" "decisiones"                                  DECISIONES.md

echo "Historial creado en $DIR/.git"
echo
git -C "$DIR" log --pretty=format:'%h  %aI  %an  %s'
echo
echo
echo "Lo que va a leer el corrector (equivalente a forense.leer_historial_git):"
echo "  commits:      $(git -C "$DIR" rev-list --count HEAD)"
echo "  autores:      $(git -C "$DIR" log --pretty=format:'%an' | sort -u | paste -sd', ' -)"
echo "  diasDeSpread: 0  (todos los commits el 2026-09-04)"

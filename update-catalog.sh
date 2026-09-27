#!/usr/bin/env bash
#
# Aggiorna il catalogo dal repository pubblicato, conservando le voci aggiunte da te.
#
# Le tue voci stanno nei file *.local.json, che git ignora: `git pull` non le tocca, e
# build_catalog.py le unisce di nuovo al catalogo pubblicato. Se hai modificato a mano i file
# tracciati, lo script si ferma invece di mescolare le due cose: sposta le modifiche nei
# *.local.json (vedi README, «Your own entries and updates»).
#
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")"

if ! git diff --quiet || ! git diff --cached --quiet; then
  echo "✋ Ci sono modifiche ai file tracciati, e un aggiornamento le mescolerebbe al catalogo"
  echo "   pubblicato:"
  git status --short --untracked-files=no
  echo "   Spostale nei file *.local.json, poi rilancia."
  exit 1
fi

echo "→ Scarico il catalogo pubblicato"
git pull --ff-only
echo "→ Rigenero il catalogo (pubblicato + voci tue)"
python3 scripts/build_catalog.py

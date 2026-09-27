#!/usr/bin/env bash
#
# Installa la skill "ai-tools-catalog" su questo computer, per tutti i coding agent.
#
# La skill segue lo standard aperto Agent Skills (https://agentskills.io): una cartella con un
# SKILL.md. La si installa in ~/.agents/skills/, la cartella comune letta da OpenCode, Codex,
# Gemini CLI, Cursor, GitHub Copilot e dagli altri agent che adottano lo standard. Due agent
# non la leggono a livello globale e ricevono un symlink alla stessa cartella: Claude Code
# (~/.claude/skills/) e Antigravity (~/.gemini/config/skills/, solo se ~/.gemini esiste).
# Una sola copia: build_catalog.py ne aggiorna una, e chi segue i symlink la vede una volta.
# Richiede python3 per rigenerare il catalogo (senza, copia i file già generati).
#
# Uso:
#   git clone <questo-repo> && cd <repo> && ./install-skill.sh
#
set -euo pipefail

SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DEST="${HOME}/.agents/skills/ai-tools-catalog"
LINKS=("${HOME}/.claude/skills/ai-tools-catalog")
[ -d "${HOME}/.gemini" ] && LINKS+=("${HOME}/.gemini/config/skills/ai-tools-catalog")

echo "→ Installo la skill in: ${DEST}"
mkdir -p "${DEST}"

for LINK in "${LINKS[@]}"; do
  # Un'installazione precedente stava direttamente in ~/.claude/skills: se è una cartella vera
  # con soli file generati, la si sostituisce col symlink. Qualunque altro contenuto è di
  # qualcun altro, e non si tocca.
  if [ -d "${LINK}" ] && [ ! -L "${LINK}" ]; then
    extra="$(find "${LINK}" -mindepth 1 -maxdepth 1 \
      ! -name SKILL.md ! -name CATALOGO-AI-TOOLS.md ! -name catalogo.json)"
    if [ -n "${extra}" ]; then
      echo "⚠️  ${LINK} contiene file non generati da questo script:"
      echo "${extra}"
      echo "   Spostali o cancellali a mano, poi rilancia."
      exit 1
    fi
    echo "→ Sostituisco la vecchia installazione in ${LINK} con un symlink"
    rm -r "${LINK}"
  fi
  mkdir -p "$(dirname "${LINK}")"
  ln -sfn "${DEST}" "${LINK}"
done

# 1) definizione della skill (statica)
cp "${SRC}/skill/SKILL.md" "${DEST}/SKILL.md"

# 2) rigenera catalogo dai dati del repo e popola la skill (CATALOGO-AI-TOOLS.md + catalogo.json)
if command -v python3 >/dev/null 2>&1; then
  python3 "${SRC}/scripts/build_catalog.py"
else
  echo "⚠️  python3 non trovato: copio i file già generati senza rigenerarli."
  cp "${SRC}/CATALOGO-AI-TOOLS.md" "${DEST}/CATALOGO-AI-TOOLS.md"
  cp "${SRC}/catalogo-unificato.json" "${DEST}/catalogo.json"
fi

echo "✅ Skill 'ai-tools-catalog' installata."
echo "   ${DEST}  (standard Agent Skills)"
for LINK in "${LINKS[@]}"; do echo "   ${LINK} → symlink"; done
echo "   Da qualsiasi progetto chiedi all'agente p.es.: \"che tool open-source esiste per fare OCR?\""

#
# Installa la skill "ai-tools-catalog" su questo computer Windows, per tutti i coding agent.
#
# La skill segue lo standard aperto Agent Skills (https://agentskills.io): una cartella con un
# SKILL.md. La si installa in %USERPROFILE%\.agents\skills\, la cartella comune letta da
# OpenCode, Codex, Gemini CLI, Cursor, GitHub Copilot e dagli altri agent che adottano lo
# standard. Due agent non la leggono a livello globale e ricevono una junction alla stessa
# cartella (non richiede privilegi di amministratore, a differenza dei symlink): Claude Code
# (.claude\skills\) e Antigravity (.gemini\config\skills\, solo se .gemini esiste).
# Richiede python3 per rigenerare il catalogo (senza, copia i file gia' generati).
#
# Uso:
#   git clone <questo-repo>; cd <repo>; .\install-skill.ps1
#

$ErrorActionPreference = "Stop"

$SRC = Split-Path -Parent $MyInvocation.MyCommand.Definition
$DEST = Join-Path $env:USERPROFILE ".agents\skills\ai-tools-catalog"
$LINKS = @(Join-Path $env:USERPROFILE ".claude\skills\ai-tools-catalog")
if (Test-Path (Join-Path $env:USERPROFILE ".gemini")) {
    $LINKS += Join-Path $env:USERPROFILE ".gemini\config\skills\ai-tools-catalog"
}

Write-Host "-> Installo la skill in: $DEST"
New-Item -ItemType Directory -Force -Path $DEST | Out-Null

foreach ($LINK in $LINKS) {
    # Un'installazione precedente stava direttamente in .claude\skills: se e' una cartella vera
    # con soli file generati, la si sostituisce con la junction. Qualunque altro contenuto non
    # si tocca.
    $item = Get-Item $LINK -ErrorAction SilentlyContinue
    if ($item -and -not $item.LinkType) {
        $generati = @("SKILL.md", "CATALOGO-AI-TOOLS.md", "catalogo.json")
        $extra = Get-ChildItem $LINK -Force | Where-Object { $generati -notcontains $_.Name }
        if ($extra) {
            Write-Host "ATTENZIONE: $LINK contiene file non generati da questo script:"
            $extra | ForEach-Object { Write-Host "  $($_.Name)" }
            Write-Host "  Spostali o cancellali a mano, poi rilancia."
            exit 1
        }
        Write-Host "-> Sostituisco la vecchia installazione in $LINK con una junction"
        Remove-Item $LINK -Recurse -Force
        $item = $null
    }
    if (-not $item) {
        New-Item -ItemType Directory -Force -Path (Split-Path -Parent $LINK) | Out-Null
        New-Item -ItemType Junction -Path $LINK -Target $DEST | Out-Null
    }
}

# 1) definizione della skill (statica)
Copy-Item "$SRC\skill\SKILL.md" "$DEST\SKILL.md" -Force

# 2) rigenera catalogo dai dati del repo e popola la skill
$pythonExe = $null
foreach ($candidate in @("python3", "python")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") {
        $pythonExe = $cmd.Source
        break
    }
}
if (-not $pythonExe) {
    foreach ($path in @("C:\Python311\python.exe", "C:\Python312\python.exe", "C:\Python313\python.exe")) {
        if (Test-Path $path) { $pythonExe = $path; break }
    }
}

if ($pythonExe) {
    & $pythonExe "$SRC\scripts\build_catalog.py"
} else {
    Write-Host "ATTENZIONE: python non trovato: copio i file gia' generati senza rigenerarli."
    Copy-Item "$SRC\CATALOGO-AI-TOOLS.md" "$DEST\CATALOGO-AI-TOOLS.md" -Force
    Copy-Item "$SRC\catalogo-unificato.json" "$DEST\catalogo.json" -Force
}

Write-Host "Skill 'ai-tools-catalog' installata."
Write-Host "  $DEST  (standard Agent Skills)"
foreach ($LINK in $LINKS) { Write-Host "  $LINK -> junction" }
Write-Host "  Da qualsiasi progetto chiedi all'agente p.es.: `"che tool open-source esiste per fare OCR?`""

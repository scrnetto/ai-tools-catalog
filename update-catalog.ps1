#
# Aggiorna il catalogo dal repository pubblicato, conservando le voci aggiunte da te.
#
# Le tue voci stanno nei file *.local.json, che git ignora: `git pull` non le tocca, e
# build_catalog.py le unisce di nuovo al catalogo pubblicato. Se hai modificato a mano i file
# tracciati, lo script si ferma invece di mescolare le due cose.
#

$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $MyInvocation.MyCommand.Definition)

$modifiche = git status --porcelain --untracked-files=no
if ($modifiche) {
    Write-Host "ATTENZIONE: ci sono modifiche ai file tracciati, e un aggiornamento le mescolerebbe"
    Write-Host "al catalogo pubblicato:"
    $modifiche | ForEach-Object { Write-Host "  $_" }
    Write-Host "Spostale nei file *.local.json, poi rilancia."
    exit 1
}

Write-Host "-> Scarico il catalogo pubblicato"
git pull --ff-only
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }

$pythonExe = $null
foreach ($candidate in @("python3", "python")) {
    $cmd = Get-Command $candidate -ErrorAction SilentlyContinue
    if ($cmd -and $cmd.Source -notlike "*WindowsApps*") { $pythonExe = $cmd.Source; break }
}
if (-not $pythonExe) { Write-Host "ATTENZIONE: python non trovato."; exit 1 }
Write-Host "-> Rigenero il catalogo (pubblicato + voci tue)"
& $pythonExe "scripts\build_catalog.py"

# PowerShell script para Windows (PowerShell)
# Uso: .\scripts\run.ps1

$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location $root\..

Write-Host "Criando/ativando virtualenv..."
if (-Not (Test-Path .\venv)) {
    python -m venv venv
}
. .\venv\Scripts\Activate.ps1

Write-Host "Instalando dependências Python..."
python -m pip install --upgrade pip
pip install -r requirements.txt

Write-Host "Iniciando backend (Flask)..."
Start-Process -FilePath python -ArgumentList 'src/app.py' -NoNewWindow -PassThru | Out-Null
Start-Sleep -Seconds 1

if (Test-Path .\frontend) {
    Write-Host "Iniciando frontend (Vite)..."
    Set-Location .\frontend
    if (-Not (Test-Path .\node_modules)) {
        npm install
    }
    npm run dev
} else {
    Write-Host "Pasta frontend não encontrada. Backend em execução na porta 5000."
    Read-Host "Pressione Enter para sair e parar o backend"
}

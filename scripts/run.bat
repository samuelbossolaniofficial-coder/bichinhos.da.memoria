@echo off
REM Script para Windows (cmd)
REM Uso: scripts\run.bat

cd /d %~dp0\..

if not exist venv (
  python -m venv venv
)
call venv\Scripts\activate.bat

python -m pip install --upgrade pip
pip install -r requirements.txt

start "backend" python src\app.py

if exist frontend (
  cd frontend
  if not exist node_modules (
    npm install
  )
  npm run dev
) else (
  echo Pasta frontend não encontrada. Backend em execução na porta 5000.
  pause
)

#!/usr/bin/env bash
set -euo pipefail

# Script para macOS / Linux: cria venv, instala dependências, inicia backend e frontend (dev).
# Uso: ./scripts/run.sh

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

echo "Criando/ativando virtualenv..."
if [ ! -d "venv" ]; then
  python3 -m venv venv
fi
# shellcheck source=/dev/null
source venv/bin/activate

echo "Instalando dependências Python..."
python -m pip install --upgrade pip
pip install -r requirements.txt

echo "Iniciando backend (Flask)..."
# roda o backend em background
python src/app.py &
PID_BACKEND=$!
echo "Backend PID: $PID_BACKEND"

# iniciar frontend
if [ -d "frontend" ]; then
  echo "Iniciando frontend (Vite)..."
  cd frontend
  # instalar node deps se necessário
  if [ ! -d "node_modules" ]; then
    npm install
  fi
  npm run dev
else
  echo "Pasta frontend não encontrada. Backend em execução na porta 5000."
  wait $PID_BACKEND
fi

# quando o dev server frontend sair, mata o backend
echo "Parando backend (PID $PID_BACKEND)..."
kill $PID_BACKEND || true

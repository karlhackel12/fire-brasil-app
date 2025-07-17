#!/bin/bash

echo "🇧🇷 FIRE Brasil - Inicializando Sistema..."
echo

echo "📋 Verificando dependências..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado. Instale Python 3.10+ primeiro."
    exit 1
fi

if ! command -v node &> /dev/null; then
    echo "❌ Node.js não encontrado. Instale Node.js 18+ primeiro."
    exit 1
fi

echo "✅ Dependências verificadas!"
echo

echo "🔧 Configurando Backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Criando ambiente virtual..."
    python3 -m venv venv
fi

echo "Ativando ambiente virtual..."
source venv/bin/activate

echo "Instalando dependências Python..."
pip install -r requirements.txt

echo "Criando diretórios necessários..."
mkdir -p data uploads logs

echo
echo "🎨 Configurando Frontend..."
cd ../frontend

echo "Instalando dependências Node.js..."
npm install

echo
echo "🚀 Inicializando Sistema..."
echo
echo "Backend estará em: http://localhost:8000"
echo "Frontend estará em: http://localhost:3000"
echo
echo "Pressione Ctrl+C para parar os serviços"
echo

# Iniciar backend em background
cd ../backend
source venv/bin/activate
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000 &
BACKEND_PID=$!

# Aguardar backend inicializar
sleep 5

# Iniciar frontend
cd ../frontend
npm start &
FRONTEND_PID=$!

echo
echo "🎉 Sistema FIRE Brasil inicializado com sucesso!"
echo
echo "PIDs dos processos:"
echo "Backend: $BACKEND_PID"
echo "Frontend: $FRONTEND_PID"
echo

# Aguardar interrupção
trap 'kill $BACKEND_PID $FRONTEND_PID; exit' INT
wait
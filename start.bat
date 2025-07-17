@echo off
echo 🇧🇷 FIRE Brasil - Inicializando Sistema...
echo.

echo 📋 Verificando dependências...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python não encontrado. Instale Python 3.10+ primeiro.
    pause
    exit /b 1
)

node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js não encontrado. Instale Node.js 18+ primeiro.
    pause
    exit /b 1
)

echo ✅ Dependências verificadas!
echo.

echo 🔧 Configurando Backend...
cd backend

if not exist venv (
    echo Criando ambiente virtual...
    python -m venv venv
)

echo Ativando ambiente virtual...
call venv\Scripts\activate

echo Instalando dependências Python...
pip install -r requirements.txt

echo Criando diretórios necessários...
if not exist data mkdir data
if not exist uploads mkdir uploads
if not exist logs mkdir logs

echo.
echo 🎨 Configurando Frontend...
cd ..\frontend

echo Instalando dependências Node.js...
npm install

echo.
echo 🚀 Inicializando Sistema...
echo.
echo Backend estará em: http://localhost:8000
echo Frontend estará em: http://localhost:3000
echo.
echo Pressione Ctrl+C para parar os serviços
echo.

start "FIRE Brasil Backend" cmd /k "cd /d %cd%\..\backend && venv\Scripts\activate && uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"

timeout /t 5 /nobreak >nul

start "FIRE Brasil Frontend" cmd /k "cd /d %cd% && npm start"

echo.
echo 🎉 Sistema FIRE Brasil inicializado com sucesso!
echo.
echo Aguarde alguns segundos para os serviços iniciarem...
echo Frontend abrirá automaticamente no navegador
echo.
pause
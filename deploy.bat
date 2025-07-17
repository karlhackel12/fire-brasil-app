@echo off
echo 🚀 FIRE Brasil - Preparação para Deploy
echo.

echo 📋 Verificando Git...
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git não encontrado. Instale Git primeiro.
    pause
    exit /b 1
)

echo ✅ Git encontrado!
echo.

echo 📦 Inicializando repositório Git...
git init

echo 📄 Adicionando arquivos ao Git...
git add .

echo 💬 Fazendo commit inicial...
git commit -m "🎉 Initial commit - FIRE Brasil App"

echo.
echo 🔗 PRÓXIMOS PASSOS:
echo.
echo 1. Crie um repositório no GitHub:
echo    https://github.com/new
echo.
echo 2. Execute os comandos:
echo    git remote add origin https://github.com/SEU-USUARIO/fire-brasil-app.git
echo    git branch -M main
echo    git push -u origin main
echo.
echo 3. Configure Railway:
echo    https://railway.app
echo    - New Project → Deploy from GitHub
echo    - Root Directory: backend
echo    - Add PostgreSQL database
echo.
echo 4. Configure Vercel:
echo    https://vercel.com
echo    - New Project → Import Git Repository
echo    - Root Directory: frontend
echo.
echo 5. Adicione variáveis de ambiente:
echo    Railway: OPENAI_API_KEY, SECRET_KEY, CORS_ORIGINS
echo    Vercel: REACT_APP_API_URL
echo.
echo 📚 Guia completo: DEPLOY.md
echo.
pause
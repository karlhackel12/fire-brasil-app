"""
Script de setup do backend FIRE Brasil
Configura ambiente, dependências e estrutura inicial
"""

import os
import sys
import subprocess
import asyncio
from pathlib import Path

def run_command(command, description):
    """Executar comando com feedback"""
    print(f"🔧 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} - Sucesso!")
            return True
        else:
            print(f"❌ {description} - Erro: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - Exceção: {str(e)}")
        return False

def setup_environment():
    """Configurar ambiente virtual e dependências"""
    print("🚀 Iniciando setup do backend FIRE Brasil...")
    
    # Verificar se está no diretório correto
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Criar ambiente virtual
    if not os.path.exists("venv"):
        if not run_command("python -m venv venv", "Criando ambiente virtual"):
            return False
    
    # Ativar ambiente virtual (Windows)
    activate_script = "venv\\Scripts\\activate" if os.name == 'nt' else "venv/bin/activate"
    
    # Instalar dependências
    pip_command = "venv\\Scripts\\pip" if os.name == 'nt' else "venv/bin/pip"
    
    if not run_command(f"{pip_command} install --upgrade pip", "Atualizando pip"):
        return False
    
    if not run_command(f"{pip_command} install -r requirements.txt", "Instalando dependências"):
        return False
    
    return True

def setup_database():
    """Configurar banco de dados SQLite"""
    print("💾 Configurando banco de dados...")
    
    # Criar diretório de dados
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Criar arquivo de configuração do banco
    db_config = """
# Configuração do banco de dados
DATABASE_URL=sqlite:///./data/fire_brasil.db
DATABASE_ECHO=false
"""
    
    with open(".env", "w") as f:
        f.write(db_config)
    
    print("✅ Banco de dados configurado!")
    return True

def setup_directories():
    """Criar estrutura de diretórios"""
    print("📁 Criando estrutura de diretórios...")
    
    directories = [
        "data",
        "uploads",
        "logs",
        "temp",
        "app/api/v1",
        "app/db",
        "app/migrations",
        "app/static",
        "app/templates"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
    
    print("✅ Estrutura de diretórios criada!")
    return True

def setup_tesseract():
    """Configurar Tesseract OCR"""
    print("👁️ Configurando Tesseract OCR...")
    
    # Verificar se Tesseract está instalado
    try:
        result = subprocess.run("tesseract --version", shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Tesseract já está instalado!")
            return True
    except:
        pass
    
    print("📥 Tesseract não encontrado. Instruções de instalação:")
    print("   Windows: Baixe em https://github.com/UB-Mannheim/tesseract/wiki")
    print("   Linux: sudo apt-get install tesseract-ocr tesseract-ocr-por")
    print("   macOS: brew install tesseract")
    
    return False

def create_startup_script():
    """Criar script de inicialização"""
    print("🚀 Criando script de inicialização...")
    
    startup_script = """#!/bin/bash
# Script de inicialização do backend FIRE Brasil

echo "🇧🇷 Iniciando FIRE Brasil Backend..."

# Ativar ambiente virtual
source venv/bin/activate

# Executar migrações do banco
python -m alembic upgrade head

# Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo "🚀 Backend rodando em http://localhost:8000"
"""
    
    with open("start.sh", "w") as f:
        f.write(startup_script)
    
    # Tornar executável no Unix
    if os.name != 'nt':
        os.chmod("start.sh", 0o755)
    
    # Criar versão Windows
    windows_script = """@echo off
echo 🇧🇷 Iniciando FIRE Brasil Backend...

REM Ativar ambiente virtual
call venv\\Scripts\\activate

REM Executar migrações do banco
python -m alembic upgrade head

REM Iniciar servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

echo 🚀 Backend rodando em http://localhost:8000
pause
"""
    
    with open("start.bat", "w") as f:
        f.write(windows_script)
    
    print("✅ Scripts de inicialização criados!")
    return True

def main():
    """Função principal do setup"""
    print("=" * 60)
    print("🇧🇷 FIRE BRASIL - SETUP DO BACKEND")
    print("=" * 60)
    
    steps = [
        ("Configurar ambiente", setup_environment),
        ("Configurar banco de dados", setup_database),
        ("Criar diretórios", setup_directories),
        ("Configurar Tesseract", setup_tesseract),
        ("Criar scripts", create_startup_script)
    ]
    
    success_count = 0
    
    for step_name, step_func in steps:
        print(f"\n📋 {step_name}...")
        if step_func():
            success_count += 1
        else:
            print(f"⚠️  {step_name} falhou, mas continuando...")
    
    print("\n" + "=" * 60)
    print(f"📊 RESUMO DO SETUP: {success_count}/{len(steps)} passos concluídos")
    print("=" * 60)
    
    if success_count >= len(steps) - 1:  # Permitir falha apenas no Tesseract
        print("✅ Setup concluído com sucesso!")
        print("\n🚀 Próximos passos:")
        print("1. Configure sua chave da OpenAI no arquivo .env")
        print("2. Instale o Tesseract OCR se necessário")
        print("3. Execute: python start.py ou ./start.sh")
        print("4. Acesse: http://localhost:8000")
    else:
        print("❌ Setup falhou. Verifique os erros acima.")
        return False
    
    return True

if __name__ == "__main__":
    main()
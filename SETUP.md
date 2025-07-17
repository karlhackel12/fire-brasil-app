# 🚀 FIRE Brasil - Guia de Instalação e Execução

## 📋 Pré-requisitos

### Obrigatórios:
- **Python 3.10+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)
- **Git** - [Download](https://git-scm.com/)

### Opcionais (mas recomendados):
- **Tesseract OCR** - Para reconhecimento de texto em imagens
- **Visual Studio Code** - Para desenvolvimento

## 🔧 Instalação do Sistema

### 1. Configurar Backend

```bash
# Navegar para a pasta do backend
cd backend

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
```

### 2. Configurar OpenAI API

Edite o arquivo `.env` e adicione sua chave da OpenAI:

```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Configurar Frontend

```bash
# Navegar para a pasta do frontend
cd ../frontend

# Instalar dependências
npm install

# Instalar dependências TypeScript (se necessário)
npm install --save-dev @types/react @types/react-dom
```

### 4. Instalar Tesseract OCR (Opcional)

**Windows:**
1. Baixar: https://github.com/UB-Mannheim/tesseract/wiki
2. Instalar e adicionar ao PATH

**Linux/Ubuntu:**
```bash
sudo apt-get install tesseract-ocr tesseract-ocr-por
```

**Mac:**
```bash
brew install tesseract
```

## 🚀 Executando o Sistema

### 1. Iniciar Backend

```bash
# Na pasta backend, com ambiente virtual ativado
cd backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará rodando em: http://localhost:8000

### 2. Iniciar Frontend

```bash
# Em um novo terminal, na pasta frontend
cd frontend
npm start
```

O frontend estará rodando em: http://localhost:3000

## 🧪 Testando o Sistema

### 1. Verificar Backend
- Acesse: http://localhost:8000
- Docs da API: http://localhost:8000/docs

### 2. Verificar Frontend
- Acesse: http://localhost:3000
- Deve aparecer o dashboard do FIRE Brasil

## 📝 Primeiros Passos

### 1. Testar Categorização de Gastos
1. Va para "Controle de Gastos"
2. Aba "Entrada Manual"
3. Adicione um gasto (ex: "Supermercado Pão de Açúcar", R$ 200)
4. Veja a categorização automática

### 2. Testar Calculadora FIRE
1. Va para "Calculadora FIRE"
2. Preencha seus dados:
   - Idade: 30
   - Renda: R$ 8.000
   - Gastos: R$ 4.800
   - Patrimônio: R$ 50.000
3. Clique em "Calcular FIRE"

### 3. Upload de Documentos
1. Va para "Controle de Gastos"
2. Aba "Upload de Documentos"
3. Teste com um PDF de extrato ou imagem de recibo

## 🔍 Solução de Problemas

### Backend não inicia:
- Verifique se o Python 3.10+ está instalado
- Confirme que o ambiente virtual está ativado
- Verifique se a chave OpenAI está configurada

### Frontend não inicia:
- Verifique se o Node.js 18+ está instalado
- Execute `npm install` novamente
- Verifique se a porta 3000 está livre

### OCR não funciona:
- Instale o Tesseract OCR
- Verifique se está no PATH do sistema
- Teste com `tesseract --version`

### Erro de conexão:
- Verifique se o backend está rodando na porta 8000
- Confirme que não há firewall bloqueando

## 📊 Estrutura de Pastas

```
fire-brasil-app/
├── backend/           # API FastAPI
│   ├── app/
│   │   ├── agents/    # Agentes IA
│   │   ├── core/      # Configurações
│   │   ├── schemas/   # Validações
│   │   └── main.py    # Aplicação principal
│   ├── requirements.txt
│   └── .env
├── frontend/          # Interface React
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   └── App.tsx
│   └── package.json
└── README.md
```

## 🎯 Funcionalidades Testáveis

### ✅ Funcionando:
- Dashboard com métricas mockadas
- Navegação entre páginas
- Interface de entrada manual
- Calculadora FIRE com simulação
- Relatórios com dados simulados

### 🔄 Em Desenvolvimento:
- Integração completa backend ↔ frontend
- Upload real de documentos
- Persistência no banco de dados
- Categorização automática em tempo real

## 🆘 Suporte

Se encontrar problemas:
1. Verifique os logs no terminal
2. Confirme que todas as dependências estão instaladas
3. Verifique se as portas não estão em uso
4. Consulte a documentação da API em /docs

## 🎉 Próximos Passos

Após o sistema funcionar:
1. Conectar frontend ao backend
2. Implementar autenticação
3. Adicionar gráficos interativos
4. Melhorar a interface mobile
5. Adicionar testes automatizados
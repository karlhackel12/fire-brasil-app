# 🚀 Guia de Deploy - FIRE Brasil

## 📋 Visão Geral

Este guia te ajudará a fazer deploy do sistema FIRE Brasil usando:
- **GitHub** - Repositório de código
- **Railway** - Backend as a Service
- **Vercel** - Frontend hosting
- **PostgreSQL** - Banco de dados na nuvem

## 🔧 Pré-requisitos

- Conta no GitHub
- Conta no Railway
- Conta no Vercel
- OpenAI API Key

## 📚 Passo a Passo

### 1. 📦 Subir para GitHub

```bash
# Inicializar repositório
cd fire-brasil-app
git init

# Adicionar arquivos
git add .
git commit -m "🎉 Initial commit - FIRE Brasil App"

# Criar repositório no GitHub e conectar
git remote add origin https://github.com/SEU-USUARIO/fire-brasil-app.git
git branch -M main
git push -u origin main
```

### 2. 🚂 Deploy Backend no Railway

#### 2.1 Configurar Railway
1. Acesse [railway.app](https://railway.app)
2. Faça login com GitHub
3. Clique em "New Project"
4. Selecione "Deploy from GitHub repo"
5. Escolha seu repositório `fire-brasil-app`

#### 2.2 Configurar Serviço Backend
1. Clique em "Add Service" → "GitHub Repo"
2. Configure:
   - **Root Directory**: `backend`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

#### 2.3 Variáveis de Ambiente
Adicione no Railway:
```env
OPENAI_API_KEY=your_openai_api_key_here
DATABASE_URL=${{PostgreSQL.DATABASE_URL}}
SECRET_KEY=fire-brasil-production-secret-2024
DEBUG=false
PORT=${{PORT}}
CORS_ORIGINS=https://fire-brasil.vercel.app
```

#### 2.4 Adicionar PostgreSQL
1. Clique em "Add Service" → "Database" → "PostgreSQL"
2. Railway criará automaticamente a `DATABASE_URL`

#### 2.5 Configurar Domínio
1. Na aba "Settings" do backend
2. Clique em "Generate Domain"
3. Anote a URL: `https://fire-brasil-api.railway.app`

### 3. ⚡ Deploy Frontend no Vercel

#### 3.1 Configurar Vercel
1. Acesse [vercel.com](https://vercel.com)
2. Faça login com GitHub
3. Clique em "New Project"
4. Importe seu repositório `fire-brasil-app`

#### 3.2 Configurar Build
1. **Root Directory**: `frontend`
2. **Build Command**: `npm run build`
3. **Output Directory**: `build`
4. **Install Command**: `npm install`

#### 3.3 Variáveis de Ambiente
Adicione no Vercel:
```env
REACT_APP_API_URL=https://fire-brasil-api.railway.app
REACT_APP_ENV=production
```

#### 3.4 Configurar Domínio
1. Na aba "Settings" → "Domains"
2. Adicione domínio customizado ou use o gerado
3. Anote a URL: `https://fire-brasil.vercel.app`

## 🔄 Configurar CI/CD

### GitHub Actions (Automático)
O deploy acontece automaticamente quando você faz push para a branch `main`.

### Monitoramento
- **Railway**: Logs em tempo real
- **Vercel**: Analytics e performance
- **GitHub**: Actions e deployment status

## 🧪 Testar Deploy

### 1. Backend
```bash
# Verificar se está funcionando
curl https://fire-brasil-api.railway.app/health

# Documentação da API
https://fire-brasil-api.railway.app/docs
```

### 2. Frontend
```bash
# Acessar aplicação
https://fire-brasil.vercel.app
```

### 3. Integração
- Frontend deve conectar com backend
- Upload de arquivos deve funcionar
- Calculadora FIRE deve responder

## 🔧 Troubleshooting

### Backend não inicia
1. Verificar logs no Railway
2. Confirmar variáveis de ambiente
3. Verificar se PostgreSQL está conectado

### Frontend não conecta ao backend
1. Verificar `REACT_APP_API_URL`
2. Confirmar CORS no backend
3. Testar endpoint manualmente

### Erro de dependências
1. Verificar `requirements.txt` e `package.json`
2. Limpar cache de build
3. Redeploy

## 📊 Monitoramento

### Railway
- CPU e RAM usage
- Logs de aplicação
- Database connections

### Vercel
- Page load times
- Build status
- Analytics

## 💰 Custos Estimados

### Railway (Backend + PostgreSQL)
- **Hobby Plan**: $5/mês
- Inclui: 512MB RAM, 1GB storage

### Vercel (Frontend)
- **Hobby Plan**: Grátis
- Inclui: 100GB bandwidth

### OpenAI API
- **Pay-as-you-go**: ~$1-5/mês
- Depende do uso

**Total estimado: $6-10/mês**

## 🔄 Atualizações

### Deploy Automático
```bash
# Fazer mudanças
git add .
git commit -m "✨ Nova funcionalidade"
git push origin main

# Deploy automático:
# - Railway: ~2-3 minutos
# - Vercel: ~1-2 minutos
```

## 🔒 Segurança

### Variáveis Sensíveis
- Nunca commitar `.env` com secrets
- Usar variáveis de ambiente do Railway/Vercel
- Rotacionar API keys periodicamente

### HTTPS
- Railway: Automático
- Vercel: Automático
- Certificados SSL inclusos

## 📞 Suporte

### Railway
- [Documentação](https://docs.railway.app)
- [Discord](https://discord.gg/railway)

### Vercel
- [Documentação](https://vercel.com/docs)
- [Discord](https://discord.gg/vercel)

## 🎉 URLs Finais

Após deploy completo:
- **Frontend**: https://fire-brasil.vercel.app
- **Backend**: https://fire-brasil-api.railway.app
- **API Docs**: https://fire-brasil-api.railway.app/docs

---

🚀 **Parabéns! Seu sistema FIRE Brasil está na nuvem!** 🇧🇷
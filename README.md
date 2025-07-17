# 🇧🇷 FIRE Brasil - Sistema de Independência Financeira

Sistema completo de controle financeiro pessoal para brasileiros alcançarem independência financeira (FIRE).

## 🚀 Demo Live

- **Frontend**: [fire-brasil.vercel.app](https://fire-brasil.vercel.app)
- **Backend API**: [fire-brasil-api.railway.app](https://fire-brasil-api.railway.app)
- **Documentação API**: [fire-brasil-api.railway.app/docs](https://fire-brasil-api.railway.app/docs)

## ✨ Funcionalidades

### 💳 Controle de Gastos
- Upload de extratos (PDF, Excel, CSV, imagens)
- OCR para reconhecimento de recibos
- Categorização automática com IA
- Input manual com validação

### 🔥 Calculadora FIRE
- Cenários brasileiros (Lean, Regular, Fat FIRE)
- Perfis de investimento adaptados ao Brasil
- Projeções personalizadas com IPCA
- Insights com OpenAI

### 📊 Dashboard Inteligente
- Métricas FIRE em tempo real
- Progresso visual para independência
- Análise de gastos por categoria
- Recomendações personalizadas

### 📈 Relatórios Detalhados
- Análise mensal automática
- Tendências e comparações
- Oportunidades de economia
- Projeções futuras

## 🛠️ Tecnologias

### Backend
- **FastAPI** - API REST moderna
- **OpenAI** - IA para categorização e insights
- **SQLAlchemy** - ORM para banco de dados
- **Tesseract** - OCR para documentos
- **Railway** - Deploy e hosting

### Frontend
- **React 18** - Interface moderna
- **TypeScript** - Tipagem estática
- **Tailwind CSS** - Estilização responsiva
- **Vercel** - Deploy e CDN

## 🚀 Deploy

### Backend (Railway)
1. Fork este repositório
2. Conecte ao Railway
3. Configure as variáveis de ambiente
4. Deploy automático

### Frontend (Vercel)
1. Conecte ao Vercel
2. Configure a pasta `frontend`
3. Adicione variáveis de ambiente
4. Deploy automático

## 🔧 Desenvolvimento Local

### Pré-requisitos
- Python 3.10+
- Node.js 18+
- OpenAI API Key

### Instalação
```bash
# Clone o repositório
git clone https://github.com/seu-usuario/fire-brasil-app.git
cd fire-brasil-app

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt

# Configurar .env
cp .env.example .env
# Adicionar OPENAI_API_KEY

# Iniciar backend
uvicorn app.main:app --reload

# Frontend (novo terminal)
cd frontend
npm install
npm start
```

### URLs Locais
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📊 Arquitetura

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   React (SPA)   │───▶│  FastAPI (REST) │───▶│   PostgreSQL    │
│   Vercel CDN    │    │  Railway Cloud  │    │  Railway Cloud  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐             │
         │              │   OpenAI API    │             │
         │              │  Categorização  │             │
         │              └─────────────────┘             │
         │                                              │
┌─────────────────┐                            ┌─────────────────┐
│   Tesseract     │                            │   File Storage  │
│   OCR Service   │                            │   Railway Vol   │
└─────────────────┘                            └─────────────────┘
```

## 🔐 Variáveis de Ambiente

### Backend (.env)
```env
OPENAI_API_KEY=sk-proj-...
DATABASE_URL=postgresql://...
SECRET_KEY=your-secret-key
DEBUG=false
CORS_ORIGINS=https://your-frontend.vercel.app
```

### Frontend (.env.local)
```env
REACT_APP_API_URL=https://your-backend.railway.app
REACT_APP_ENV=production
```

## 🇧🇷 Características Brasileiras

- **Moeda**: Todos os valores em Reais (R$)
- **Inflação**: Cálculos com IPCA
- **Investimentos**: Tesouro Direto, CDB, LCI, FIIs
- **Categorias**: Adaptadas ao contexto brasileiro
- **Impostos**: Considera IR sobre investimentos

## 📱 Funcionalidades Móveis

- Interface responsiva
- Upload via câmera
- Notificações push (futuro)
- App PWA (futuro)

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -m 'Add nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja [LICENSE](LICENSE) para mais detalhes.

## 🎯 Roadmap

### V1.0 ✅
- [x] Dashboard básico
- [x] Controle de gastos
- [x] Calculadora FIRE
- [x] Categorização IA
- [x] Deploy Vercel + Railway

### V1.1 🔄
- [ ] Autenticação de usuários
- [ ] Banco de dados persistente
- [ ] Upload real de documentos
- [ ] Gráficos interativos

### V2.0 📋
- [ ] App mobile
- [ ] Integração bancos
- [ ] Notificações inteligentes
- [ ] Comunidade FIRE

## 👨‍💻 Desenvolvedor

**Seu Nome**
- GitHub: [@seu-usuario](https://github.com/seu-usuario)
- LinkedIn: [Seu Nome](https://linkedin.com/in/seu-perfil)
- Email: seu@email.com

---

⭐ Se este projeto te ajudou, dê uma estrela!

🔥 **Rumo à Independência Financeira!** 🇧🇷
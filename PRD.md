# PRD - FIRE Brasil App

## 📋 Visão Geral do Produto

### Título
**FIRE Brasil - Aplicativo de Independência Financeira**

### Versão
1.0.0

### Data
Janeiro 2025

### Responsável
Karl Hackel

---

## 🎯 Resumo Executivo

### Propósito
O FIRE Brasil é uma aplicação web completa para controle financeiro pessoal focada em ajudar brasileiros a alcançar a independência financeira (FIRE - Financial Independence, Retire Early) adaptada à realidade econômica do Brasil.

### Problema
- Brasileiros têm dificuldade em controlar gastos e planejar aposentadoria
- Falta de ferramentas adaptadas à realidade brasileira (inflação IPCA, investimentos locais)
- Ausência de orientação personalizada para independência financeira
- Categorização manual de gastos é demorada e imprecisa

### Solução
Aplicativo web com IA que automatiza categorização de gastos, calcula cenários FIRE brasileiros e fornece consultoria financeira personalizada através de agentes inteligentes.

---

## 🎭 Personas

### Persona Principal: "João, o Profissional Planejador"
- **Idade**: 28-45 anos
- **Perfil**: Profissional liberal, renda R$ 5.000-15.000/mês
- **Objetivo**: Aposentar aos 50-55 anos
- **Dores**: Não sabe quanto economizar, gastos descontrolados
- **Comportamento**: Usa apps financeiros, planilhas Excel

### Persona Secundária: "Maria, a Empreendedora"
- **Idade**: 25-40 anos
- **Perfil**: Empreendedora, renda variável
- **Objetivo**: Segurança financeira e crescimento patrimonial
- **Dores**: Renda irregular, dificuldade em categorizar gastos
- **Comportamento**: Prefere automação, gosta de relatórios visuais

---

## 🎯 Objetivos do Produto

### Objetivos Primários
1. **Automatizar controle financeiro** - Reduzir tempo de categorização em 80%
2. **Calcular cenários FIRE** - Fornecer projeções realistas para aposentadoria
3. **Orientação personalizada** - IA que analisa perfil e sugere melhorias
4. **Adaptação brasileira** - Considerar inflação IPCA e investimentos locais

### Objetivos Secundários
1. **Educação financeira** - Ensinar conceitos FIRE
2. **Gamificação** - Tornar controle financeiro engajante
3. **Relatórios inteligentes** - Insights automáticos sobre gastos
4. **Integração futura** - Preparar para Open Banking

### Métricas de Sucesso
- **Retenção**: 70% dos usuários ativos após 30 dias
- **Engagement**: 5+ transações categorizadas por semana
- **Satisfação**: NPS > 50
- **Conversão**: 15% dos usuários calculam FIRE regularmente

---

## 🛠 Funcionalidades

### MVP (Versão 1.0)

#### 1. Autenticação e Onboarding
- **Login/Cadastro** - Email/senha
- **Onboarding** - Questionário inicial sobre perfil financeiro
- **Tutorial** - Guia de primeiros passos

#### 2. Controle de Gastos
- **Entrada Manual** - Formulário para adicionar gastos
- **Upload de Documentos** - PDF, Excel, CSV, imagens
- **OCR Inteligente** - Extração automática de dados de recibos
- **Categorização IA** - OpenAI categoriza gastos automaticamente
- **Categorias Brasileiras** - Alimentação, Transporte, Moradia, etc.

#### 3. Calculadora FIRE
- **Cenários FIRE** - Lean, Regular, Fat, Coast, Barista
- **Regra 25x Adaptada** - Considerando inflação IPCA
- **Simulações** - Diferentes aportes e rendimentos
- **Tipos de Investimento** - Tesouro Direto, CDB, LCI/LCA, Ações

#### 4. Dashboard e Relatórios
- **Visão Geral** - Resumo financeiro mensal
- **Progresso FIRE** - Indicadores visuais de progresso
- **Gráficos Interativos** - Gastos por categoria, evolução temporal
- **Insights IA** - Análises automáticas e sugestões

#### 5. Agentes Inteligentes
- **Processador de Documentos** - OCR e extração estruturada
- **Categorizador** - IA para classificação automática
- **Calculadora FIRE** - Projeções e cenários
- **Consultor Financeiro** - Dicas personalizadas

### Roadmap Futuro (v2.0+)

#### Funcionalidades Avançadas
- **Metas Financeiras** - Definir e acompanhar objetivos
- **Alertas Inteligentes** - Notificações de gastos excessivos
- **Comparação Social** - Benchmarks anônimos
- **Simulador de Aposentadoria** - Diferentes cenários de vida

#### Integrações
- **Open Banking** - Conexão automática com bancos
- **Plataformas de Investimento** - Acompanhar carteira
- **Receita Federal** - Importar dados do IR
- **API Banco Central** - Taxas e indicadores atualizados

---

## 🏗 Arquitetura Técnica

### Frontend
- **Framework**: React 18 + TypeScript
- **Styling**: Tailwind CSS + Headless UI
- **Roteamento**: React Router 6
- **Gráficos**: Chart.js + React Chart.js 2
- **Formulários**: React Hook Form
- **Estado**: Context API + useState/useEffect

### Backend
- **Framework**: FastAPI + Python 3.10
- **Banco de Dados**: PostgreSQL (produção), SQLite (desenvolvimento)
- **IA**: OpenAI GPT-4 para categorização e insights
- **OCR**: Tesseract + OpenCV para processamento de imagens
- **Documentos**: PDFPlumber, OpenPyXL para extração
- **Autenticação**: JWT + bcrypt

### Infraestrutura
- **Frontend**: Vercel (CDN global)
- **Backend**: Railway (containers)
- **Banco**: Railway PostgreSQL
- **Armazenamento**: Railway volumes
- **Monitoramento**: Railway logs + métricas

### Integrações
- **OpenAI API** - Categorização e insights
- **Tesseract OCR** - Reconhecimento de texto
- **MCP (Model Context Protocol)** - Orquestração de agentes

---

## 🎨 Design e UX

### Princípios de Design
1. **Simplicidade** - Interface clean e intuitiva
2. **Responsividade** - Funcionar em mobile e desktop
3. **Acessibilidade** - Seguir padrões WCAG
4. **Brasileirismo** - Cores, linguagem e contexto local

### Paleta de Cores
- **Primária**: Verde brasileiro (#28A745)
- **Secundária**: Azul confiança (#007BFF)
- **Neutros**: Cinzas (#F8F9FA, #6C757D)
- **Alertas**: Vermelho (#DC3545), Amarelo (#FFC107)

### Componentes Principais
- **Cards** - Exibir métricas e informações
- **Formulários** - Entrada de dados consistente
- **Tabelas** - Listagem de transações
- **Gráficos** - Visualizações interativas
- **Modais** - Ações secundárias

---

## 📊 Fluxos de Usuário

### Fluxo Principal: Adicionar Gasto
1. **Usuário** acessa "Controle de Gastos"
2. **Escolhe método**: Manual ou Upload
3. **Se Manual**: Preenche formulário
4. **Se Upload**: Faz upload do documento
5. **Sistema** processa com OCR + IA
6. **Usuário** confirma categorização
7. **Sistema** salva e atualiza dashboard

### Fluxo Secundário: Calcular FIRE
1. **Usuário** acessa "Calculadora FIRE"
2. **Preenche dados**: Idade, renda, gastos, patrimônio
3. **Escolhe cenário**: Lean, Regular, Fat FIRE
4. **Sistema** calcula projeções
5. **Usuário** visualiza resultados
6. **Sistema** salva cenário para acompanhamento

---

## 🔒 Segurança e Privacidade

### Dados Sensíveis
- **Criptografia** - Senhas com bcrypt
- **HTTPS** - Comunicação segura
- **Tokens JWT** - Autenticação stateless
- **Sanitização** - Validação de inputs

### Privacidade
- **LGPD** - Conformidade com lei brasileira
- **Anonimização** - Dados agregados sem identificação
- **Consentimento** - Opt-in para coleta de dados
- **Direito ao Esquecimento** - Exclusão de dados

### Backup e Recuperação
- **Backups Diários** - Railway automated backups
- **Versionamento** - Git para código
- **Monitoramento** - Logs e alertas
- **Disaster Recovery** - Plano de contingência

---

## 📈 Estratégia de Lançamento

### Fase 1: MVP (Meses 1-2)
- **Funcionalidades básicas** - Controle de gastos e FIRE
- **Usuários Beta** - 50 usuários para feedback
- **Validação** - Testar hipóteses principais

### Fase 2: Refinamento (Meses 3-4)
- **Melhorias UX** - Based on user feedback
- **Performance** - Otimizações de velocidade
- **Bugs** - Correções e estabilidade

### Fase 3: Escala (Meses 5-6)
- **Marketing** - Lançamento público
- **Funcionalidades Avançadas** - Metas, alertas
- **Integrações** - Preparar Open Banking

---

## 💰 Modelo de Negócio

### Freemium
- **Gratuito** - Até 100 transações/mês
- **Premium** - R$ 9,90/mês - Transações ilimitadas
- **Pro** - R$ 19,90/mês - Consultoria IA avançada

### Custos Operacionais
- **Infraestrutura** - ~R$ 50/mês (Railway + Vercel)
- **OpenAI API** - ~R$ 100/mês (varia com uso)
- **Domínio** - ~R$ 50/ano
- **Total Estimado** - R$ 200/mês

### Projeção de Receita
- **Ano 1** - 100 usuários premium = R$ 1.000/mês
- **Ano 2** - 500 usuários premium = R$ 5.000/mês
- **Ano 3** - 2.000 usuários premium = R$ 20.000/mês

---

## 🎯 Riscos e Mitigações

### Riscos Técnicos
- **API OpenAI** - Instabilidade ou mudanças de preço
  - *Mitigação*: Implementar fallbacks e cache
- **Limite de Requisições** - Throttling da OpenAI
  - *Mitigação*: Rate limiting e queue system

### Riscos de Negócio
- **Concorrência** - Apps financeiros grandes
  - *Mitigação*: Foco em nicho FIRE brasileiro
- **Regulação** - Mudanças em leis financeiras
  - *Mitigação*: Compliance e adaptação contínua

### Riscos Operacionais
- **Escalabilidade** - Crescimento inesperado
  - *Mitigação*: Arquitetura cloud-native
- **Segurança** - Vazamento de dados
  - *Mitigação*: Auditorias e melhores práticas

---

## 📋 Cronograma de Desenvolvimento

### Sprint 1-2 (Semanas 1-4): Backend Foundation
- [ ] Configurar infraestrutura (Railway, Vercel)
- [ ] Implementar autenticação JWT
- [ ] Criar agentes MCP básicos
- [ ] Integrar OpenAI API

### Sprint 3-4 (Semanas 5-8): Core Features
- [ ] Controle de gastos (manual + upload)
- [ ] Categorização automática
- [ ] Calculadora FIRE básica
- [ ] Dashboard inicial

### Sprint 5-6 (Semanas 9-12): UX e Polish
- [ ] Interface responsiva
- [ ] Gráficos interativos
- [ ] Relatórios detalhados
- [ ] Testes e otimizações

### Sprint 7-8 (Semanas 13-16): Launch Prep
- [ ] Testes de usuário
- [ ] Documentação
- [ ] Monitoramento
- [ ] Marketing materials

---

## 🎉 Definição de Sucesso

### Métricas Primárias
- **Usuários Ativos** - 100 MAU (Monthly Active Users)
- **Retenção** - 70% após 30 dias
- **Categorização** - 90% de precisão da IA
- **FIRE Calculations** - 50% dos usuários calculam mensalmente

### Métricas Secundárias
- **Performance** - <2s tempo de carregamento
- **Uptime** - 99.5% disponibilidade
- **Satisfação** - NPS > 50
- **Conversão** - 15% free-to-paid

---

## 📞 Contato e Aprovações

### Stakeholders
- **Product Owner**: Karl Hackel
- **Developer**: Karl Hackel
- **Users**: Beta testers community

### Aprovações
- [x] Requisitos técnicos validados
- [x] Arquitetura aprovada
- [x] Design system definido
- [ ] Orçamento aprovado
- [ ] Timeline confirmada

---

**Este PRD é um documento vivo e será atualizado conforme o produto evolui.**

*Última atualização: Janeiro 2025*
# 🏭 API Ordem da Fenix - Monitoramento Industrial

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Fly.io](https://img.shields.io/badge/Fly.io-8B5CF6?style=for-the-badge&logo=fly.io&logoColor=white)

> **API robusta para monitoramento de compressores industriais com sistema de alertas inteligente e atualização automática de status**

## 🚀 **Deploy Ativo**

- **🌐 URL Produção:** https://ordem-da-fenix-api.fly.dev/
- **📚 Documentação:** https://ordem-da-fenix-api.fly.dev/docs
- **🔍 Health Check:** https://ordem-da-fenix-api.fly.dev/health
- **⚙️ Configurações:** https://ordem-da-fenix-api.fly.dev/configuracoes

---

## 📋 **Funcionalidades**

### 🏭 **Gestão de Compressores**
- ✅ CRUD completo de compressores (15-37 kW)
- ✅ Validação de dados com Pydantic
- ✅ Status automático (ligado/desligado) via sensores
- ✅ Controle de última atualização e manutenção
- ✅ Suporte a múltiplas marcas e localizações

### 📊 **Sistema de Monitoramento Avançado**
- ✅ Coleta de dados de sensores em tempo real
- ✅ **7 parâmetros monitorados:**
  - Pressão (0-15 bar)
  - Temperatura do equipamento (60-110°C)
  - Temperatura ambiente (-10 a 50°C)
  - Potência/Consumo (15-45 kW)
  - Umidade ambiente (0-100%)
  - Vibração anormal (detecção booleana)
  - Status liga/desliga automático
- ✅ Histórico completo de medições
- ✅ Filtros por compressor e período
- ✅ Atualização automática do status do compressor

### 🚨 **Sistema de Alertas Inteligente (5 Níveis)**
Sistema avançado baseado em parâmetros industriais reais:

| Nível | Cor | Faixa | Descrição | Ação Requerida |
|-------|-----|-------|-----------|----------------|
| 🔵 **Muito Baixo** | Azul | 0-20% | Parâmetros muito abaixo | Verificação de funcionamento |
| 🟡 **Baixo** | Amarelo | 20-40% | Performance reduzida | Monitoramento contínuo |
| 🟢 **Normal** | Verde | 40-70% | Operação ideal | Nenhuma ação necessária |
| 🟠 **Alto** | Laranja | 70-85% | Parâmetros elevados | Atenção necessária |
| 🔴 **Crítico** | Vermelho | 85-100% | Risco de falha | **Intervenção Imediata** |

### 🔧 **Parâmetros Detalhados**

#### **Pressão (bar)**
- Muito Baixo: 0.0 - 5.0
- Baixo: 5.0 - 7.0  
- **Normal: 7.0 - 10.0** ✅
- Alto: 10.0 - 11.0
- Crítico: > 11.0

#### **Temperatura Equipamento (°C)**
- Muito Baixo: 0 - 60
- Baixo: 60 - 71
- **Normal: 71 - 82** ✅
- Alto: 82 - 107
- Crítico: > 107

#### **Temperatura Ambiente (°C)**
- Muito Baixo: -10 - 0
- Baixo: 0 - 10
- **Normal: 10 - 29** ✅
- Alto: 29 - 46
- Crítico: > 46

#### **Potência/Consumo (kW)**
- Muito Baixo: 0 - 10
- Baixo: 10 - 15
- **Normal: 15 - 37** ✅
- Alto: 37 - 45
- Crítico: > 45

#### **Umidade (%)**
- Muito Baixo: 0 - 20 (muito seco)
- Baixo: 20 - 40 (seco)
- **Normal: 40 - 70** ✅
- Alto: 70 - 85 (úmido)
- Crítico: 85 - 100 (risco condensação)

#### **Vibração**
- **Normal**: Sem vibração anormal detectada ✅
- **Crítico**: Vibração anormal detectada (problema mecânico)

---

## 🛠 **Tecnologias**

- **Backend:** FastAPI 0.119+
- **Database:** Firebase Firestore
- **Auth:** Firebase Admin SDK
- **Deploy:** Fly.io (São Paulo, Brasil)
- **Docs:** Swagger/OpenAPI 3.0
- **Timezone:** America/Sao_Paulo (UTC-3)
- **CORS:** Configurado para GitHub Pages

---

## 🎯 **Endpoints Completos**

### 🩺 **System**
```http
GET /health                    # Health check detalhado
GET /configuracoes             # Parâmetros do sistema
GET /configuracoes/info        # Informações sobre o sistema
```

### 🏭 **Compressores**  
```http
GET    /compressores                   # Listar todos
GET    /compressores?ativo_apenas=true # Filtrar por status
GET    /compressores?limit=10          # Limitar resultados
POST   /compressores                   # Criar novo
GET    /compressores/{id}              # Buscar específico
PUT    /compressores/{id}              # Atualizar
DELETE /compressores/{id}              # Remover
```

### 📊 **Sensores**
```http
POST /sensor                           # Enviar dados do sensor
GET  /dados                            # Todos os dados de sensores
GET  /dados/{id_compressor}            # Dados de compressor específico
GET  /dados/{id_compressor}?limit=10   # Últimos N registros
```

---

## 🔄 **Fluxo de Funcionamento**

1. **Cadastro**: Compressor é registrado via POST `/compressores`
2. **Monitoramento**: Sensor envia dados via POST `/sensor`
3. **Processamento Automático**:
   - Dados salvos no Firestore
   - Status do compressor atualizado automaticamente
   - Alertas gerados em tempo real
   - Timestamp brasileiro aplicado
4. **Consulta**: Frontend acessa dados via GET endpoints

---

## 📡 **Modelo de Dados do Sensor**

```json
{
  "id_compressor": 1001,
  "ligado": true,
  "pressao": 8.5,
  "temp_equipamento": 75.0,
  "temp_ambiente": 25.0,
  "potencia_kw": 22.0,
  "umidade": 55.0,
  "vibracao": false,
  "data_medicao": "2025-10-17T10:30:00-03:00"
}
```

## 🏗️ **Modelo de Dados do Compressor**

```json
{
  "id_compressor": 1001,
  "nome_marca": "Atlas Copco GA22",
  "localizacao": "Setor A - Linha 1",
  "potencia_nominal_kw": 22.0,
  "configuracao": "Compressor Médio-Padrão",
  "data_ultima_manutencao": "2025-10-15T14:30:00-03:00",
  "esta_ligado": true,
  "data_ultima_atualizacao": "2025-10-17T10:30:00-03:00",
  "alertas": {
    "pressao": "normal",
    "temperatura_equipamento": "normal",
    "temperatura_ambiente": "normal",
    "potencia": "normal",
    "umidade": "normal",
    "vibracao": "normal"
  }
}
```

---

## 🚀 **Configuração Local**

### **1. Clone e Setup**
```bash
git clone https://github.com/Ordem-da-Fenix/API.git
cd API
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac  
source venv/bin/activate
```

### **2. Dependências**
```bash
pip install -r requirements.txt
```

### **3. Configuração Firebase**
```bash
# Opção 1: Arquivo JSON (recomendado para desenvolvimento)
# Copie seu serviceAccountKey.json para a raiz do projeto

# Opção 2: Variáveis de ambiente (produção)
cp .env.example .env
# Edite o .env com suas credenciais Firebase
```

### **4. Executar**
```bash
uvicorn app.main:app --reload --port 8000
```

**Acesse:** http://localhost:8000/docs

---

## 🌐 **Deploy no Fly.io**

### **Pré-requisitos**
- Conta no [Fly.io](https://fly.io)
- [Fly CLI](https://fly.io/docs/getting-started/installing-flyctl/) instalado

### **Deploy Completo**
```bash
# 1. Login
fly auth login

# 2. Configurar secrets Firebase
fly secrets set FIREBASE_PROJECT_ID="your-project-id"
fly secrets set FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
fly secrets set FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxx@project.iam.gserviceaccount.com"

# 3. Deploy
fly deploy

# 4. Verificar
fly status
fly logs
```

### **Configuração Fly.io**
- **Região:** São Paulo (gru)
- **Port:** 8000
- **Health Check:** `/health` a cada 30s
- **Auto-scaling:** 0-1 máquinas
- **Recursos:** 1 CPU, 512MB RAM

---

## 📊 **Estrutura do Projeto**

```
API/
├── 📁 app/                    # Código principal
│   ├── 📁 api/               # Endpoints
│   │   ├── compressores.py   # CRUD compressores
│   │   ├── sensors.py        # Dados sensores + status automático
│   │   └── configuracoes.py  # Configurações do sistema
│   ├── 📁 db/                # Database
│   │   └── firebase.py       # Conexão Firebase multi-método
│   ├── 📁 models/            # Modelos Pydantic
│   │   ├── compressor.py     # Modelo compressor + status automático
│   │   ├── sensor.py         # Modelo sensor (7 parâmetros)
│   │   └── parametros.py     # Configurações avançadas
│   ├── 📁 utils/             # Utilitários
│   │   ├── alertas.py        # Sistema alertas 5 níveis
│   │   ├── datetime_utils.py # Timezone brasileiro (UTC-3)
│   │   └── error_handling.py # Tratamento erros + logging
│   └── main.py               # App principal + CORS
├── 📄 fly.toml               # Config Fly.io
├── 📄 Procfile               # Config deploy
├── 📄 requirements.txt       # Dependências
├── 📄 .env.example           # Template variáveis
├── 📄 .gitignore             # Arquivos ignorados
└── 📄 README.md              # Esta documentação
```

---

## 🧪 **Testes da API**

### **Health Check**
```bash
curl https://ordem-da-fenix-api.fly.dev/health
```

### **Criar Compressor**
```bash
curl -X POST https://ordem-da-fenix-api.fly.dev/compressores \
  -H "Content-Type: application/json" \
  -d '{
    "id_compressor": 1001,
    "nome_marca": "Atlas Copco GA22", 
    "localizacao": "Setor A - Linha 1",
    "potencia_nominal_kw": 22.0
  }'
```

### **Enviar Dados do Sensor**
```bash
curl -X POST https://ordem-da-fenix-api.fly.dev/sensor \
  -H "Content-Type: application/json" \
  -d '{
    "id_compressor": 1001,
    "ligado": true,
    "pressao": 8.5,
    "temp_equipamento": 75.0,
    "temp_ambiente": 25.0,
    "potencia_kw": 22.0,
    "umidade": 55.0,
    "vibracao": false
  }'
```

### **Consultar Dados**
```bash
# Listar compressores
curl https://ordem-da-fenix-api.fly.dev/compressores

# Dados do sensor
curl https://ordem-da-fenix-api.fly.dev/dados/1001?limit=5

# Configurações do sistema
curl https://ordem-da-fenix-api.fly.dev/configuracoes
```

---

## 📈 **Monitoramento**

### **Logs em Tempo Real**
```bash
# Logs gerais
fly logs --app ordem-da-fenix-api

# Logs de erro apenas
fly logs --app ordem-da-fenix-api --grep ERROR

# Logs das últimas 2 horas
fly logs --app ordem-da-fenix-api --since 2h
```

### **Métricas e Status**
- **Dashboard:** https://fly.io/apps/ordem-da-fenix-api/monitoring
- **Health Check:** Automático a cada 30s
- **Uptime:** Monitorado pelo Fly.io
- **Logs Estruturados:** Com timestamp brasileiro

---

## 🔒 **Segurança**

### **CORS Configurado**
```python
allowed_origins = [
    "http://localhost:3000",           # React dev
    "http://localhost:5500",           # Live Server
    "https://ordem-da-fenix.github.io", # GitHub Pages
    "https://ordem-da-fenix.vercel.app", # Vercel
]
```

### **Firebase Security**
- Service Account Key protegida
- Variáveis de ambiente criptografadas
- Conexão SSL/TLS obrigatória

### **Validação de Dados**
- Pydantic para validação automática
- Ranges específicos para cada parâmetro
- Tratamento de exceções completo

---

## 🚨 **Alertas e Notificações**

### **Sistema de Alertas Ativo**
Quando um sensor envia dados, o sistema:

1. ✅ Salva os dados no Firestore
2. ✅ Atualiza o status do compressor automaticamente
3. ✅ Gera alertas para todos os 7 parâmetros
4. ✅ Armazena alertas no documento do compressor
5. ✅ Registra logs estruturados

### **Exemplos de Alertas**
```json
{
  "pressao": "normal",
  "temperatura_equipamento": "alto", 
  "temperatura_ambiente": "normal",
  "potencia": "normal",
  "umidade": "critico",
  "vibracao": "normal"
}
```

---

## ⚡ **Performance**

### **Otimizações Implementadas**
- ✅ **Thread-safe operations** com `run_in_threadpool`
- ✅ **Firestore queries otimizadas** (limitadas e indexadas)
- ✅ **Logs estruturados** com níveis apropriados
- ✅ **Error handling robusto** com exceções específicas
- ✅ **Timezone handling** otimizado para Brasil
- ✅ **Auto-scaling** no Fly.io (0-1 máquinas)

### **Limites e Capacidade**
- **Concurrent Connections:** 25 hard limit, 20 soft limit
- **Query Limits:** 50-1000 registros por consulta
- **Response Time:** < 500ms para operações normais
- **Memory Usage:** 512MB por máquina

---

## 🔮 **Roadmap**

### **Próximas Versões**
- [ ] Sistema de usuários e autenticação
- [ ] WebSocket para dados em tempo real
- [ ] Dashboard de métricas avançadas
- [ ] Alertas via email/SMS
- [ ] Backup automático de dados
- [ ] API de relatórios em PDF
- [ ] Integração com sistemas ERP

---

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Siga os padrões de código Python (PEP 8)
4. Teste suas alterações localmente
5. Commit suas mudanças (`git commit -m 'Add: AmazingFeature'`)
6. Push para a branch (`git push origin feature/AmazingFeature`)
7. Abra um Pull Request

### **Padrões de Commit**
- `feat:` Nova funcionalidade
- `fix:` Correção de bug
- `docs:` Alterações na documentação
- `style:` Formatação de código
- `refactor:` Refatoração de código
- `test:` Adição de testes

---

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

---

## 👨‍💻 **Desenvolvedor**

**Ordem da Fenix** - Sistema de Monitoramento Industrial  
📧 Email: contato@ordemdafenix.com.br  
🌐 Website: [ordemdafenix.com.br](https://ordemdafenix.com.br)  
📱 GitHub: [@Ordem-da-Fenix](https://github.com/Ordem-da-Fenix)

---

## 📊 **Status do Projeto**

![Build Status](https://img.shields.io/badge/build-passing-brightgreen)
![API Status](https://img.shields.io/badge/API-online-brightgreen)
![Coverage](https://img.shields.io/badge/coverage-85%25-yellowgreen)
![Version](https://img.shields.io/badge/version-1.0.0-blue)

### **Última Atualização**
- **Data:** 17 de outubro de 2025
- **Versão:** 1.0.0
- **Features:** Sistema completo de monitoramento com 7 parâmetros
- **Status:** ✅ Em produção estável

---

<div align="center">

**⚡ Desenvolvido com FastAPI + Firebase + Fly.io ⚡**

![Stars](https://img.shields.io/github/stars/Ordem-da-Fenix/API?style=social)
![Forks](https://img.shields.io/github/forks/Ordem-da-Fenix/API?style=social)
![Issues](https://img.shields.io/github/issues/Ordem-da-Fenix/API)

**🏭 Monitoramento Industrial de Precisão 🏭**

</div>
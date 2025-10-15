# 🏭 API Ordem da Fenix - Monitoramento Industrial

![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Fly.io](https://img.shields.io/badge/Fly.io-8B5CF6?style=for-the-badge&logo=fly.io&logoColor=white)

> **API robusta para monitoramento de compressores industriais com sistema de alertas inteligente**

## 🚀 **Deploy Ativo**

- **🌐 URL Produção:** https://ordem-da-fenix-api.fly.dev/
- **📚 Documentação:** https://ordem-da-fenix-api.fly.dev/docs
- **🔍 Health Check:** https://ordem-da-fenix-api.fly.dev/health

---

## 📋 **Funcionalidades**

### 🏭 **Gestão de Compressores**
- ✅ CRUD completo de compressores (15-37 kW)
- ✅ Validação de dados com Pydantic
- ✅ Suporte a múltiplas marcas (Atlas Copco, Schulz, Ingersoll Rand)

### 📊 **Sistema de Monitoramento**
- ✅ Coleta de dados de sensores em tempo real
- ✅ Histórico completo de medições
- ✅ Filtros por data e período

### 🚨 **Sistema de Alertas Inteligente**
Sistema de 5 níveis baseado em parâmetros industriais:

| Nível | Cor | Descrição | Ação Requerida |
|-------|-----|-----------|----------------|
| 🔵 **Muito Baixo** | Azul | Parâmetros abaixo do mínimo | Verificação |
| 🟡 **Baixo** | Amarelo | Performance reduzida | Monitoramento |
| 🟢 **Normal** | Verde | Operação ideal | Nenhuma |
| 🟠 **Alto** | Laranja | Parâmetros elevados | Atenção |
| 🔴 **Crítico** | Vermelho | Risco de falha | **Intervenção Imediata** |

### 🔧 **Parâmetros Monitorados**
- **Pressão:** 0-15 bar
- **Temperatura:** 0-100°C  
- **Vibração:** 0-5 mm/s
- **Corrente Elétrica:** 0-50 A
- **Horas de Operação:** Contador acumulativo

---

## 🛠 **Tecnologias**

- **Backend:** FastAPI 0.119+
- **Database:** Firebase Firestore
- **Auth:** Firebase Admin SDK
- **Deploy:** Fly.io
- **Docs:** Swagger/OpenAPI 3.0

---

## 🎯 **Endpoints Principais**

### 🩺 **System**
```http
GET /health                    # Health check
GET /configuracoes            # Parâmetros do sistema
```

### 🏭 **Compressores**  
```http
GET    /compressores          # Listar todos
POST   /compressores          # Criar novo
GET    /compressores/{id}     # Buscar específico
PUT    /compressores/{id}     # Atualizar
DELETE /compressores/{id}     # Remover
```

### 📊 **Sensores**
```http
POST /sensores/{id}/dados                    # Enviar medição
GET  /sensores/{id}/historico               # Histórico completo
GET  /sensores/{id}/historico?limite=10     # Últimos N registros
GET  /sensores/{id}/historico?data_inicio=...&data_fim=...  # Por período
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
# Copie seu serviceAccountKey.json para a raiz do projeto
# Configure as variáveis de ambiente:
cp .env.example .env
```

### **4. Executar**
```bash
uvicorn app.main:app --reload --port 8000
```

---

## 🌐 **Deploy no Fly.io**

### **Pré-requisitos**
- Conta no [Fly.io](https://fly.io)
- Fly CLI instalado

### **Deploy**
```bash
# 1. Login
fly auth login

# 2. Configurar secrets
fly secrets set FIREBASE_PROJECT_ID="your-project-id"
fly secrets set FIREBASE_PRIVATE_KEY="-----BEGIN PRIVATE KEY-----..."
fly secrets set FIREBASE_CLIENT_EMAIL="firebase-adminsdk-xxx@project.iam.gserviceaccount.com"

# 3. Deploy
fly deploy
```

---

## 📊 **Estrutura do Projeto**

```
API/
├── 📁 app/                    # Código principal
│   ├── 📁 api/               # Endpoints
│   │   ├── compressores.py   # CRUD compressores
│   │   ├── sensors.py        # Dados sensores
│   │   └── configuracoes.py  # Configurações
│   ├── 📁 db/                # Database
│   │   └── firebase.py       # Conexão Firebase
│   ├── 📁 models/            # Modelos Pydantic
│   │   ├── compressor.py     # Modelo compressor
│   │   └── sensor.py         # Modelo sensor
│   ├── 📁 utils/             # Utilitários
│   │   ├── alertas.py        # Sistema alertas
│   │   ├── datetime_utils.py # Manipulação datas
│   │   └── error_handling.py # Tratamento erros
│   └── main.py               # App principal
├── 📄 fly.toml               # Config Fly.io
├── 📄 Procfile               # Config deploy
├── 📄 requirements.txt       # Dependências
└── 📄 README.md              # Documentação
```

---

## 🧪 **Testes da API**

### **Via cURL**
```bash
# Health check
curl https://ordem-da-fenix-api.fly.dev/health

# Listar compressores  
curl https://ordem-da-fenix-api.fly.dev/compressores

# Criar compressor
curl -X POST https://ordem-da-fenix-api.fly.dev/compressores \
  -H "Content-Type: application/json" \
  -d '{
    "id_compressor": 1001,
    "nome_marca": "Atlas Copco GA22", 
    "localizacao": "Setor A",
    "potencia_nominal_kw": 22.0
  }'
```

### **Via Insomnia/Postman**
Importe o arquivo `insomnia_atualizado.json` com coleção completa de testes.

---

## 📈 **Monitoramento**

### **Logs**
```bash
# Logs em tempo real
fly logs --app ordem-da-fenix-api

# Logs específicos
fly logs --app ordem-da-fenix-api --since 1h
```

### **Métricas**
- **Dashboard:** https://fly.io/apps/ordem-da-fenix-api/monitoring
- **Status:** Health check automático a cada 30s

---

## 🤝 **Contribuição**

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

---

## 📝 **Licença**

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para detalhes.

---

## 👨‍💻 **Desenvolvedor**

**Ordem da Fenix** - Sistema de Monitoramento Industrial  
📧 Email: contato@ordemdafenix.com.br  
🌐 Website: [ordemdafenix.com.br](https://ordemdafenix.com.br)

---

<div align="center">

**⚡ Desenvolvido com FastAPI + Firebase + Fly.io ⚡**

![Stars](https://img.shields.io/github/stars/Ordem-da-Fenix/API?style=social)
![Forks](https://img.shields.io/github/forks/Ordem-da-Fenix/API?style=social)
![Issues](https://img.shields.io/github/issues/Ordem-da-Fenix/API)

</div>
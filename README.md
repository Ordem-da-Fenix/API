# API - Ordem da Fenix

API FastAPI para coleta de dados de sensores com integração Firebase Firestore.

## Estrutura do Projeto

```
main.py                 # entrypoint da aplicação
firebase.py             # configuração Firebase (temporário)
app/
  main.py              # factory da aplicação FastAPI
  api/
    sensors.py         # endpoints de sensores
  models/
    sensor.py          # modelos Pydantic
  db/
    firebase.py        # camada de dados
```

## Endpoints

- `POST /sensor` - Recebe dados de sensores (compressor_temp, ambiente_temp, pressure)
- `GET /dados` - Retorna todos os dados salvos
- `GET /ping` - Health check

## Como executar

1. Ative o ambiente virtual:
```powershell
. .\venv\Scripts\Activate.ps1
```

2. Execute a aplicação:
```powershell
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

3. Acesse a documentação: http://127.0.0.1:8000/docs

## Configuração Firebase

⚠️ **Importante**: As credenciais Firebase foram movidas para fora do código para segurança.

### Opções de configuração (em ordem de prioridade):

1. **Arquivo JSON** (recomendado para desenvolvimento local):
   - Coloque `serviceAccountKey.json` no diretório raiz do projeto
   - Este arquivo está no `.gitignore` e não será versionado

2. **Variável de ambiente com JSON completo**:
   ```bash
   export FIREBASE_SERVICE_ACCOUNT='{"type":"service_account",...}'
   ```

3. **Variáveis individuais no arquivo `.env`**:
   - Copie `.env.example` para `.env`
   - Preencha as variáveis `FIREBASE_PROJECT_ID`, `FIREBASE_PRIVATE_KEY`, etc.

### Obter credenciais Firebase:
1. Acesse [Firebase Console](https://console.firebase.google.com/)
2. Vá em Project Settings > Service Accounts
3. Clique em "Generate new private key"
4. Salve o arquivo como `serviceAccountKey.json` no projeto

"""Inicialização e configuração do Firebase Firestore."""
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()


def load_credentials():
    """Carrega credenciais do Firebase de diferentes fontes."""
    # 1) Arquivo serviceAccountKey.json no diretório raiz
    key_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 
                           'serviceAccountKey.json')
    if os.path.exists(key_path):
        return credentials.Certificate(key_path)

    # 2) Variável de ambiente FIREBASE_SERVICE_ACCOUNT (JSON completo)
    sa_json = os.environ.get('FIREBASE_SERVICE_ACCOUNT')
    if sa_json:
        try:
            sa_dict = json.loads(sa_json)
            return credentials.Certificate(sa_dict)
        except Exception:
            pass

    # 3) Variáveis de ambiente individuais do Firebase (.env)
    if all([
        os.environ.get('FIREBASE_PROJECT_ID'),
        os.environ.get('FIREBASE_PRIVATE_KEY'),
        os.environ.get('FIREBASE_CLIENT_EMAIL')
    ]):
        # Processa a chave privada para garantir quebras de linha corretas
        private_key = os.environ.get('FIREBASE_PRIVATE_KEY')
        if private_key:
            private_key = private_key.replace('\\n', '\n')
        
        return credentials.Certificate({
            "type": "service_account",
            "project_id": os.environ.get('FIREBASE_PROJECT_ID'),
            "private_key_id": os.environ.get('FIREBASE_PRIVATE_KEY_ID'),
            "private_key": private_key,
            "client_email": os.environ.get('FIREBASE_CLIENT_EMAIL'),
            "client_id": os.environ.get('FIREBASE_CLIENT_ID'),
            "auth_uri": os.environ.get('FIREBASE_AUTH_URI'),
            "token_uri": os.environ.get('FIREBASE_TOKEN_URI'),
            "auth_provider_x509_cert_url": os.environ.get('FIREBASE_AUTH_PROVIDER_X509_CERT_URL'),
            "client_x509_cert_url": os.environ.get('FIREBASE_CLIENT_X509_CERT_URL'),
            "universe_domain": "googleapis.com"
        })
    
    # 4) Se nada funcionar, erro
    raise RuntimeError(
        'Firebase não pôde ser inicializado. Configure:\n'
        '1) serviceAccountKey.json no diretório raiz, ou\n'
        '2) variável FIREBASE_SERVICE_ACCOUNT com JSON completo, ou\n'
        '3) variáveis individuais no .env (FIREBASE_PROJECT_ID, FIREBASE_PRIVATE_KEY, etc.)'
    )


# Inicializar Firebase
cred = load_credentials()
if not firebase_admin._apps:  # Evita inicializar múltiplas vezes
    firebase_admin.initialize_app(cred)

db = firestore.client()

"""Utilitários para tratamento de erros e logging."""
import logging
from typing import Any, Callable, Optional
from fastapi import HTTPException
from firebase_admin import exceptions as firebase_exceptions

# Configurar logger
logger = logging.getLogger(__name__)


class FirestoreError(Exception):
    """Exceção personalizada para erros do Firestore."""
    pass


def handle_firestore_exceptions(func: Callable) -> Callable:
    """Decorator para tratamento de exceções do Firestore."""
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except firebase_exceptions.NotFoundError as e:
            logger.warning(f"Documento não encontrado: {str(e)}")
            raise HTTPException(status_code=404, detail="Documento não encontrado")
        except firebase_exceptions.AlreadyExistsError as e:
            logger.warning(f"Documento já existe: {str(e)}")
            raise HTTPException(status_code=409, detail="Documento já existe")
        except firebase_exceptions.PermissionDeniedError as e:
            logger.error(f"Permissão negada no Firestore: {str(e)}")
            raise HTTPException(status_code=403, detail="Acesso negado ao banco de dados")
        except firebase_exceptions.UnavailableError as e:
            logger.error(f"Firestore indisponível: {str(e)}")
            raise HTTPException(status_code=503, detail="Serviço de banco de dados temporariamente indisponível")
        except firebase_exceptions.DeadlineExceededError as e:
            logger.error(f"Timeout no Firestore: {str(e)}")
            raise HTTPException(status_code=504, detail="Timeout na operação do banco de dados")
        except firebase_exceptions.ResourceExhaustedError as e:
            logger.error(f"Recursos esgotados no Firestore: {str(e)}")
            raise HTTPException(status_code=429, detail="Muitas requisições. Tente novamente em alguns segundos")
        except Exception as e:
            logger.error(f"Erro inesperado no Firestore: {str(e)}")
            raise HTTPException(status_code=500, detail="Erro interno do servidor")
    
    return wrapper


def log_operation(operation: str, entity_type: str, entity_id: Optional[str] = None):
    """Log estruturado para operações."""
    def decorator(func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            entity_info = f" [{entity_id}]" if entity_id else ""
            logger.info(f"Iniciando {operation} em {entity_type}{entity_info}")
            
            try:
                result = func(*args, **kwargs)
                logger.info(f"Sucesso {operation} em {entity_type}{entity_info}")
                return result
            except Exception as e:
                logger.error(f"Erro {operation} em {entity_type}{entity_info}: {str(e)}")
                raise
        
        return wrapper
    return decorator


def setup_logging():
    """Configura logging para a aplicação."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler('app.log', encoding='utf-8')
        ]
    )
    
    # Reduzir verbosidade de bibliotecas externas
    logging.getLogger('google').setLevel(logging.WARNING)
    logging.getLogger('firebase_admin').setLevel(logging.WARNING)
    logging.getLogger('grpc').setLevel(logging.WARNING)
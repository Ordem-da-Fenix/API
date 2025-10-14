from fastapi import APIRouter
from ..utils.alertas import obter_configuracao_fixa
import logging

logger = logging.getLogger(__name__)
router = APIRouter(tags=["configuracoes"], prefix="/configuracoes")


@router.get("/", response_model=dict)
async def obter_configuracao():
    """Obtém a configuração fixa do sistema de monitoramento."""
    logger.info("Buscando configuração fixa do sistema")
    
    configuracao = obter_configuracao_fixa()
    
    return {
        "status": "sucesso",
        "message": "Configuração obtida com sucesso",
        **configuracao
    }


@router.get("/info", response_model=dict)
async def informacoes_sistema():
    """Informações sobre o sistema de monitoramento."""
    return {
        "projeto": "Monitoramento de Compressores Industriais",
        "versao": "1.0",
        "data_criacao": "2025-10-13",
        "tipo_configuracao": "Fixa - Compressor de Teste",
        "funcionalidades": {
            "monitoramento_tempo_real": "Avaliação contínua de parâmetros",
            "alertas_integrados": "Alertas incluídos nos dados do compressor",
            "configuracao_fixa": "Limites pré-definidos para teste"
        },
        "parametros_monitorados": [
            "pressao",
            "temperatura_equipamento", 
            "temperatura_ambiente"
        ],
        "niveis_alerta": [
            "muito_baixo",
            "baixo", 
            "normal",
            "alto",
            "critico"
        ]
    }
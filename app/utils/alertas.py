from typing import Dict, Any
from ..models.sensor import SensorData
from ..utils.datetime_utils import now_br
import logging

logger = logging.getLogger(__name__)

# Configurações fixas para o compressor de teste - 5 níveis
CONFIGURACAO_FIXA = {
    "limites_pressao": {
        "muito_baixo": {"min": 0.0, "max": 4.0},
        "baixo": {"min": 4.0, "max": 6.0},
        "normal": {"min": 6.0, "max": 8.0},
        "alto": {"min": 8.0, "max": 9.0},
        "critico": {"min": 9.0, "max": float('inf')}
    },
    "limites_temp_equipamento": {
        "muito_baixo": {"min": 0.0, "max": 15.0},
        "baixo": {"min": 15.0, "max": 25.0},
        "normal": {"min": 25.0, "max": 70.0},
        "alto": {"min": 70.0, "max": 85.0},
        "critico": {"min": 85.0, "max": float('inf')}
    },
    "limites_temp_ambiente": {
        "muito_baixo": {"min": 0.0, "max": 10.0},
        "baixo": {"min": 10.0, "max": 18.0},
        "normal": {"min": 18.0, "max": 28.0},
        "alto": {"min": 28.0, "max": 35.0},
        "critico": {"min": 35.0, "max": float('inf')}
    }
}

def avaliar_nivel(valor: float, limites: Dict[str, Dict[str, float]]) -> str:
    """Avalia o nível de um valor baseado nos limites configurados (5 níveis)."""
    # Verificar em ordem: critico -> alto -> normal -> baixo -> muito_baixo
    niveis_ordem = ["critico", "alto", "normal", "baixo", "muito_baixo"]
    
    for nivel in niveis_ordem:
        limite = limites[nivel]
        if limite["min"] <= valor <= limite["max"]:
            return nivel
    
    # Fallback para normal se não encontrar correspondência
    return "normal"

def gerar_alertas(sensor_data: SensorData) -> Dict[str, str]:
    """Gera alertas baseados nos dados do sensor e nas configurações fixas."""
    logger.info(f"Gerando alertas para compressor {sensor_data.id_compressor}")
    
    alertas = {}
    
    # Avaliar pressão
    alertas["pressao"] = avaliar_nivel(sensor_data.pressao, CONFIGURACAO_FIXA["limites_pressao"])
    
    # Avaliar temperatura do equipamento
    alertas["temperatura_equipamento"] = avaliar_nivel(
        sensor_data.temp_equipamento, 
        CONFIGURACAO_FIXA["limites_temp_equipamento"]
    )
    
    # Avaliar temperatura ambiente
    alertas["temperatura_ambiente"] = avaliar_nivel(
        sensor_data.temp_ambiente, 
        CONFIGURACAO_FIXA["limites_temp_ambiente"]
    )
    
    # Log dos alertas gerados
    alertas_anormais = {k: v for k, v in alertas.items() if v != "normal"}
    if alertas_anormais:
        logger.warning(f"Alertas detectados no compressor {sensor_data.id_compressor}: {alertas_anormais}")
    else:
        logger.info(f"Todos os parâmetros normais no compressor {sensor_data.id_compressor}")
    
    return alertas

def obter_configuracao_fixa() -> Dict[str, Any]:
    """Retorna a configuração fixa do sistema."""
    return {
        "configuracao": CONFIGURACAO_FIXA,
        "descricao": "Configuração fixa para compressor de teste",
        "versao": "1.0",
        "data_aplicacao": now_br(),
        "niveis_alerta": {
            "muito_baixo": {"cor": "azul", "descricao": "Valor muito baixo - verificar funcionamento"},
            "baixo": {"cor": "amarelo", "descricao": "Valor baixo - monitorar operação"},
            "normal": {"cor": "verde", "descricao": "Operação dentro dos parâmetros normais"},
            "alto": {"cor": "laranja", "descricao": "Valor alto - atenção necessária"},
            "critico": {"cor": "vermelho", "descricao": "Valor crítico - intervenção imediata"}
        }
    }
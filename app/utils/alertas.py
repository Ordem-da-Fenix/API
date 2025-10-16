from typing import Dict, Any
from ..models.sensor import SensorData
from ..utils.datetime_utils import now_br
import logging

logger = logging.getLogger(__name__)

# Configurações baseadas em Compressores Médios (15-37 kW) - 5 níveis
CONFIGURACAO_FIXA = {
    "limites_pressao": {
        "muito_baixo": {"min": 0.0, "max": 5.0},
        "baixo": {"min": 5.0, "max": 7.0},
        "normal": {"min": 7.0, "max": 10.0},
        "alto": {"min": 10.0, "max": 11.0},
        "critico": {"min": 11.0, "max": float('inf')}
    },
    "limites_temp_equipamento": {
        "muito_baixo": {"min": 0.0, "max": 60.0},
        "baixo": {"min": 60.0, "max": 71.0},
        "normal": {"min": 71.0, "max": 82.0},
        "alto": {"min": 82.0, "max": 107.0},
        "critico": {"min": 107.0, "max": float('inf')}
    },
    "limites_temp_ambiente": {
        "muito_baixo": {"min": -10.0, "max": 0.0},
        "baixo": {"min": 0.0, "max": 10.0},
        "normal": {"min": 10.0, "max": 29.0},
        "alto": {"min": 29.0, "max": 46.0},
        "critico": {"min": 46.0, "max": float('inf')}
    },
    "limites_potencia": {
        "muito_baixo": {"min": 0.0, "max": 10.0},
        "baixo": {"min": 10.0, "max": 15.0},
        "normal": {"min": 15.0, "max": 37.0},
        "alto": {"min": 37.0, "max": 45.0},
        "critico": {"min": 45.0, "max": float('inf')}
    },
    "limites_umidade": {
        "muito_baixo": {"min": 0.0, "max": 20.0},
        "baixo": {"min": 20.0, "max": 40.0},
        "normal": {"min": 40.0, "max": 70.0},
        "alto": {"min": 70.0, "max": 85.0},
        "critico": {"min": 85.0, "max": 100.0}
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
    
    # Avaliar potência/consumo
    alertas["potencia"] = avaliar_nivel(
        sensor_data.potencia_kw, 
        CONFIGURACAO_FIXA["limites_potencia"]
    )
    
    # Avaliar umidade
    alertas["umidade"] = avaliar_nivel(
        sensor_data.umidade, 
        CONFIGURACAO_FIXA["limites_umidade"]
    )
    
    # Avaliar vibração (booleano - crítico se detectada)
    alertas["vibracao"] = "critico" if sensor_data.vibracao else "normal"
    
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
        "descricao": "Compressores Médios (15-37 kW) - Faixa intermediária ideal",
        "categoria": "compressores_medios",
        "faixa_potencia": "15-37 kW",
        "versao": "1.1",
        "data_aplicacao": now_br(),
        "especificacoes_gerais": {
            "potencia_kw": {"minimo": 15, "maximo": 37, "ideal": 22},
            "pressao_bar": {"minimo": 7, "maximo": 10, "padrao": 8.5},
            "temperatura_equipamento": {
                "minimo_operacional": 71,
                "maximo_operacional": 82,
                "maximo_seguro": 107,
                "desligamento_automatico": 110
            },
            "temperatura_ambiente": {
                "minimo_ideal": 10,
                "maximo_ideal": 29,
                "minimo_operacional": 0,
                "maximo_operacional": 46
            },
            "umidade_percentual": {
                "minimo_ideal": 40,
                "maximo_ideal": 70,
                "minimo_operacional": 20,
                "maximo_operacional": 85,
                "critico": 85
            },
            "vibracao": {
                "normal": "sem_vibracao_anormal",
                "critico": "vibracao_detectada",
                "descricao": "Detecção de vibração anormal indica possível problema mecânico"
            }
        },
        "vantagens": [
            "Temperaturas operacionais mais baixas (71-82°C)",
            "Limite térmico conservador (107°C)",
            "Pressão universal 7-10 bar",
            "Ciclo de trabalho 100% sem estresse térmico",
            "Maior vida útil dos componentes",
            "Melhor relação custo-benefício"
        ],
        "niveis_alerta": {
            "muito_baixo": {"cor": "azul", "descricao": "Valor muito baixo - verificar funcionamento"},
            "baixo": {"cor": "amarelo", "descricao": "Valor baixo - monitorar operação"},
            "normal": {"cor": "verde", "descricao": "Operação dentro dos parâmetros normais"},
            "alto": {"cor": "laranja", "descricao": "Valor alto - atenção necessária"},
            "critico": {"cor": "vermelho", "descricao": "Valor crítico - intervenção imediata"}
        }
    }
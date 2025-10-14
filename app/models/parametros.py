from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, List
from enum import Enum


class PrioridadeAlerta(str, Enum):
    """Níveis de prioridade para alertas."""
    informativo = "informativo"
    atencao = "atencao" 
    alta = "alta"
    critica = "critica"


class LimitesPressao(BaseModel):
    """Limites operacionais de pressão."""
    minimo: float = Field(..., ge=0, description="Pressão mínima (bar)")
    ideal_minimo: float = Field(..., ge=0, description="Pressão ideal mínima (bar)")
    ideal_maximo: float = Field(..., ge=0, description="Pressão ideal máxima (bar)")
    maximo: float = Field(..., ge=0, description="Pressão máxima (bar)")
    critico: float = Field(..., ge=0, description="Pressão crítica (bar)")


class LimitesTemperatura(BaseModel):
    """Limites operacionais de temperatura."""
    minimo: float = Field(..., description="Temperatura mínima (°C)")
    ideal_minimo: float = Field(..., description="Temperatura ideal mínima (°C)")
    ideal_maximo: float = Field(..., description="Temperatura ideal máxima (°C)")
    maximo: float = Field(..., description="Temperatura máxima (°C)")
    critico: float = Field(..., description="Temperatura crítica (°C)")


class ConfiguracaoAlerta(BaseModel):
    """Configuração de um alerta específico."""
    limite: float = Field(..., description="Valor limite para disparar alerta")
    prioridade: PrioridadeAlerta = Field(..., description="Prioridade do alerta")
    mensagem: str = Field(..., min_length=1, max_length=200, description="Mensagem do alerta")
    ativo: bool = Field(default=True, description="Se o alerta está ativo")


class ConfiguracaoParametros(BaseModel):
    """Configuração completa de parâmetros para um compressor."""
    id_compressor: int = Field(..., gt=0, description="ID do compressor")
    
    # Limites operacionais
    limites_pressao: LimitesPressao = Field(..., description="Limites de pressão")
    limites_temp_ambiente: LimitesTemperatura = Field(..., description="Limites temperatura ambiente")
    limites_temp_equipamento: LimitesTemperatura = Field(..., description="Limites temperatura equipamento")
    
    # Alertas de pressão
    alerta_pressao_baixa: ConfiguracaoAlerta = Field(..., description="Alerta pressão baixa")
    alerta_pressao_alta: ConfiguracaoAlerta = Field(..., description="Alerta pressão alta")
    alerta_pressao_critica: ConfiguracaoAlerta = Field(..., description="Alerta pressão crítica")
    
    # Alertas de temperatura
    alerta_temp_ambiente_baixa: ConfiguracaoAlerta = Field(..., description="Alerta temperatura ambiente baixa")
    alerta_temp_ambiente_alta: ConfiguracaoAlerta = Field(..., description="Alerta temperatura ambiente alta")
    alerta_temp_equipamento_alta: ConfiguracaoAlerta = Field(..., description="Alerta temperatura equipamento alta")
    
    # Configurações gerais
    frequencia_leitura_segundos: int = Field(default=5, ge=1, le=3600, description="Frequência de leitura em segundos")
    aplicacao_especifica: Optional[str] = Field(default=None, description="Aplicação específica (ferramentas_pneumaticas, pintura_industrial, etc.)")


class ConfiguracaoParametrosUpdate(BaseModel):
    """Modelo para atualização de configurações."""
    limites_pressao: Optional[LimitesPressao] = None
    limites_temp_ambiente: Optional[LimitesTemperatura] = None
    limites_temp_equipamento: Optional[LimitesTemperatura] = None
    alerta_pressao_baixa: Optional[ConfiguracaoAlerta] = None
    alerta_pressao_alta: Optional[ConfiguracaoAlerta] = None
    alerta_pressao_critica: Optional[ConfiguracaoAlerta] = None
    alerta_temp_ambiente_baixa: Optional[ConfiguracaoAlerta] = None
    alerta_temp_ambiente_alta: Optional[ConfiguracaoAlerta] = None
    alerta_temp_equipamento_alta: Optional[ConfiguracaoAlerta] = None
    frequencia_leitura_segundos: Optional[int] = Field(default=None, ge=1, le=3600)
    aplicacao_especifica: Optional[str] = None


class ConfiguracaoParametrosOut(ConfiguracaoParametros):
    """Modelo para resposta da API."""
    firestore_id: str = Field(..., description="ID do documento no Firestore")
    data_criacao: datetime = Field(..., description="Data de criação da configuração")
    data_ultima_atualizacao: Optional[datetime] = Field(default=None, description="Data da última atualização")


class PresetAplicacao(BaseModel):
    """Preset de configuração para aplicações específicas."""
    nome: str = Field(..., description="Nome da aplicação")
    descricao: str = Field(..., description="Descrição da aplicação")
    limites_pressao: LimitesPressao = Field(..., description="Limites de pressão recomendados")
    limites_temp_ambiente: LimitesTemperatura = Field(..., description="Limites temperatura ambiente")
    limites_temp_equipamento: LimitesTemperatura = Field(..., description="Limites temperatura equipamento")
    frequencia_leitura_segundos: int = Field(..., ge=1, le=3600, description="Frequência recomendada")


class AlertaAtivo(BaseModel):
    """Modelo para alertas ativos no sistema."""
    id_compressor: int = Field(..., gt=0, description="ID do compressor")
    tipo_alerta: str = Field(..., description="Tipo do alerta")
    prioridade: PrioridadeAlerta = Field(..., description="Prioridade do alerta")
    mensagem: str = Field(..., description="Mensagem do alerta")
    valor_atual: float = Field(..., description="Valor atual que disparou o alerta")
    valor_limite: float = Field(..., description="Valor limite configurado")
    data_disparo: datetime = Field(..., description="Data e hora do disparo")
    ativo: bool = Field(default=True, description="Se o alerta ainda está ativo")
    reconhecido: bool = Field(default=False, description="Se o alerta foi reconhecido pelo operador")
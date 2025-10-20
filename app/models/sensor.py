from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SensorData(BaseModel):
    """Modelo para dados recebidos do sensor de compressor (compatibilidade)."""
    id_compressor: int = Field(..., gt=0, description="ID único do compressor (número inteiro positivo)")
    ligado: bool = Field(..., description="Status do compressor (ligado/desligado)")
    pressao: float = Field(..., ge=0, description="Pressão atual em bar")
    temp_equipamento: float = Field(..., description="Temperatura do equipamento em °C")
    temp_ambiente: float = Field(..., description="Temperatura ambiente em °C")
    potencia_kw: float = Field(..., ge=0, description="Consumo de energia em kW")
    umidade: float = Field(..., ge=0, le=100, description="Percentual de umidade do ambiente em %")
    vibracao: bool = Field(..., description="Detecção de vibração anormal (true=detectada, false=normal)")
    corrente: float = Field(..., ge=0, description="Corrente elétrica em amperes (A)")
    data_medicao: Optional[datetime] = Field(default=None, description="Data e hora da medição (opcional, será preenchida automaticamente se não informada)")


class ESP32AlertasData(BaseModel):
    """Modelo para atualização de alertas do ESP32 no compressor."""
    id_compressor: int = Field(..., gt=0, description="ID único do compressor (número inteiro positivo)")
    
    # Alertas calculados pelo ESP32 (6 parâmetros) - strings com 3 níveis possíveis
    alerta_potencia: str = Field(..., description="Nível de alerta para potência (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    alerta_pressao: str = Field(..., description="Nível de alerta para pressão (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    alerta_temperatura_ambiente: str = Field(..., description="Nível de alerta para temperatura ambiente (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    alerta_temperatura_equipamento: str = Field(..., description="Nível de alerta para temperatura equipamento (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    alerta_umidade: str = Field(..., description="Nível de alerta para umidade (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    alerta_corrente: str = Field(..., description="Nível de alerta para corrente elétrica (3 níveis: abaixo_do_normal, normal, acima_do_normal)")
    
    # Vibração é apenas booleano (true=vibrando, false=normal)
    vibracao: bool = Field(..., description="Detecção de vibração anormal (true=detectada, false=normal)")
    
    data_medicao: Optional[datetime] = Field(default=None, description="Data e hora da medição (opcional, será preenchida automaticamente se não informada)")


class SensorOut(SensorData):
    """Modelo para dados retornados pela API."""
    firestore_id: str = Field(..., description="ID do documento no Firestore")
    data_medicao: datetime = Field(..., description="Data e hora da medição (sempre preenchida)")


class ESP32AlertasOut(BaseModel):
    """Modelo para resposta da atualização de alertas do ESP32."""
    id_compressor: int = Field(..., description="ID do compressor atualizado")
    alertas_atualizados: dict = Field(..., description="Alertas que foram atualizados")
    data_atualizacao: datetime = Field(..., description="Data e hora da atualização dos alertas")

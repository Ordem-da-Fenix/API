from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class SensorData(BaseModel):
    """Modelo para dados recebidos do sensor de compressor."""
    id_compressor: int = Field(..., gt=0, description="ID único do compressor (número inteiro positivo)")
    ligado: bool = Field(..., description="Status do compressor (ligado/desligado)")
    pressao: float = Field(..., ge=0, description="Pressão atual em bar")
    temp_equipamento: float = Field(..., description="Temperatura do equipamento em °C")
    temp_ambiente: float = Field(..., description="Temperatura ambiente em °C")
    potencia_kw: float = Field(..., ge=0, description="Consumo de energia em kW")
    umidade: float = Field(..., ge=0, le=100, description="Percentual de umidade do ambiente em %")
    vibracao: bool = Field(..., description="Detecção de vibração anormal (true=detectada, false=normal)")
    data_medicao: Optional[datetime] = Field(default=None, description="Data e hora da medição (opcional, será preenchida automaticamente se não informada)")


class SensorOut(SensorData):
    """Modelo para dados retornados pela API."""
    firestore_id: str = Field(..., description="ID do documento no Firestore")
    data_medicao: datetime = Field(..., description="Data e hora da medição (sempre preenchida)")

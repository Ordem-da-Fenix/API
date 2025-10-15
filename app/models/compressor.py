from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CompressorData(BaseModel):
    """Modelo para dados de cadastro de compressor médio (15-37 kW)."""
    id_compressor: int = Field(..., gt=0, description="ID único do compressor (número inteiro positivo)")
    nome_marca: str = Field(..., min_length=1, max_length=100, description="Nome/marca do compressor")
    localizacao: str = Field(..., min_length=1, max_length=200, description="Localização do compressor")
    potencia_nominal_kw: float = Field(..., ge=15, le=37, description="Potência nominal em kW (faixa média: 15-37 kW)")
    configuracao: str = Field(default="Compressor Médio-Padrão", description="Configuração do compressor")
    data_ultima_manutencao: Optional[datetime] = Field(default=None, description="Data da última manutenção")
    esta_ligado: bool = Field(default=False, description="Status atual do compressor (ligado/desligado)")
    data_ultima_atualizacao: Optional[datetime] = Field(default=None, description="Data da última atualização de status via sensor")


class CompressorOut(CompressorData):
    """Modelo para dados retornados pela API."""
    firestore_id: str = Field(..., description="ID do documento no Firestore")
    data_cadastro: datetime = Field(..., description="Data e hora do cadastro")


class CompressorUpdate(BaseModel):
    """Modelo para atualização de dados do compressor médio."""
    nome_marca: Optional[str] = Field(default=None, description="Nome/marca do compressor")
    localizacao: Optional[str] = Field(default=None, description="Localização do compressor")
    potencia_nominal_kw: Optional[float] = Field(default=None, ge=15, le=37, description="Potência nominal em kW (faixa média: 15-37 kW)")
    configuracao: Optional[str] = Field(default=None, description="Configuração do compressor")
    data_ultima_manutencao: Optional[datetime] = Field(default=None, description="Data da última manutenção")
    esta_ligado: Optional[bool] = Field(default=None, description="Status atual do compressor")
    data_ultima_atualizacao: Optional[datetime] = Field(default=None, description="Data da última atualização de status via sensor")
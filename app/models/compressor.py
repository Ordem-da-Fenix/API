from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CompressorData(BaseModel):
    """Modelo para dados de cadastro de compressor."""
    id_compressor: int = Field(..., gt=0, description="ID único do compressor (número inteiro positivo)")
    nome_marca: str = Field(..., min_length=1, max_length=100, description="Nome/marca do compressor")
    localizacao: str = Field(..., min_length=1, max_length=200, description="Localização do compressor")
    data_ultima_manutencao: Optional[datetime] = Field(default=None, description="Data da última manutenção")
    esta_ligado: bool = Field(default=False, description="Status atual do compressor (ligado/desligado)")


class CompressorOut(CompressorData):
    """Modelo para dados retornados pela API."""
    firestore_id: str = Field(..., description="ID do documento no Firestore")
    data_cadastro: datetime = Field(..., description="Data e hora do cadastro")


class CompressorUpdate(BaseModel):
    """Modelo para atualização de dados do compressor."""
    nome_marca: Optional[str] = Field(default=None, description="Nome/marca do compressor")
    localizacao: Optional[str] = Field(default=None, description="Localização do compressor")
    data_ultima_manutencao: Optional[datetime] = Field(default=None, description="Data da última manutenção")
    esta_ligado: Optional[bool] = Field(default=None, description="Status atual do compressor")
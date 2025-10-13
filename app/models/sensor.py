from pydantic import BaseModel


class SensorData(BaseModel):
    compressor_temp: float
    ambiente_temp: float
    pressure: float


class SensorOut(SensorData):
    id: str

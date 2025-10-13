from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool
from ..models.sensor import SensorData
from ..db.firebase import db

router = APIRouter(tags=["sensors"])


@router.post("/sensor")
async def receive_sensor_data(data: SensorData):
	# Salva os dados no Firestore
	doc_ref = db.collection("sensores").add(data.dict())
	return {"message": "Dados recebidos com sucesso", "firestore_id": doc_ref[1].id, "data": data}


@router.get("/dados")
async def get_sensor_data():
	# Buscar dados em threadpool para não bloquear o loop async
	sensores = await run_in_threadpool(lambda: list(db.collection("sensores").stream()))
	dados = {doc.id: doc.to_dict() for doc in sensores}
	return {"dados": dados}


@router.get("/ping")
async def ping():
    return {"message": "pong"}

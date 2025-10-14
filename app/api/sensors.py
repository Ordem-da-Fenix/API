from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from ..models.sensor import SensorData, SensorOut
from ..db.firebase import db
from ..utils.datetime_utils import now_br
from ..utils.error_handling import handle_firestore_exceptions
from ..utils.alertas import gerar_alertas
from typing import List, Optional, Dict
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["sensors"])


async def atualizar_alertas_compressor(id_compressor: int, alertas: Dict[str, str]):
	"""Atualiza os alertas nas informações do compressor."""
	try:
		@handle_firestore_exceptions
		def atualizar_alertas():
			# Buscar o compressor
			docs = list(db.collection("compressores").where("id_compressor", "==", id_compressor).limit(1).stream())
			if not docs:
				return False
			
			doc = docs[0]
			# Atualizar com os novos alertas
			doc.reference.update({
				"alertas": alertas,
				"ultima_atualizacao_alertas": now_br()
			})
			return True
		
		sucesso = await run_in_threadpool(atualizar_alertas)
		if sucesso:
			logger.info(f"Alertas atualizados para compressor {id_compressor}: {alertas}")
		else:
			logger.warning(f"Compressor {id_compressor} não encontrado para atualizar alertas")
			
	except Exception as e:
		logger.error(f"Erro ao atualizar alertas do compressor {id_compressor}: {str(e)}")


@router.post("/sensor")
async def receive_sensor_data(data: SensorData):
	"""Recebe e armazena dados do sensor no Firestore."""
	logger.info(f"Recebendo dados do sensor para compressor {data.id_compressor}")
	try:
		# Verificar se o compressor existe
		@handle_firestore_exceptions
		def verificar_compressor():
			docs = list(db.collection("compressores").where("id_compressor", "==", data.id_compressor).limit(1).stream())
			return len(docs) > 0
		
		compressor_existe = await run_in_threadpool(verificar_compressor)
		if not compressor_existe:
			logger.warning(f"Tentativa de envio de dados para compressor inexistente: {data.id_compressor}")
			raise HTTPException(
				status_code=404,
				detail=f"Compressor com ID {data.id_compressor} não encontrado. Cadastre o compressor primeiro."
			)
		
		# Preencher data_medicao se não foi informada
		data_dict = data.model_dump()
		if data_dict["data_medicao"] is None:
			data_dict["data_medicao"] = now_br()
		
		# Salvar no Firestore de forma thread-safe
		@handle_firestore_exceptions
		def add_to_firestore():
			doc_ref = db.collection("sensor_data").add(data_dict)
			return doc_ref[1].id
		
		doc_id = await run_in_threadpool(add_to_firestore)
		
		# Atualizar alertas do compressor baseado nesta leitura
		alertas = gerar_alertas(data)
		await atualizar_alertas_compressor(data.id_compressor, alertas)
		
		logger.info(f"Dados do sensor salvos com sucesso (ID: {doc_id}) e alertas atualizados: {alertas}")
	
		return {
			"status": "sucesso",
			"message": "Dados do sensor salvos com sucesso",
			"firestore_id": doc_id,
			"id_compressor": data_dict["id_compressor"],
			"data_medicao": data_dict["data_medicao"]
		}
	except Exception as e:
		logger.error(f"Erro inesperado ao salvar dados do sensor: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Erro ao salvar dados do sensor: {str(e)}")


@router.get("/dados")
async def get_sensor_data():
	"""Busca todos os dados dos sensores armazenados."""
	logger.info("Buscando todos os dados dos sensores")
	try:
		@handle_firestore_exceptions
		def fetch_data():
			docs = list(db.collection("sensor_data").order_by("data_medicao", direction="DESCENDING").stream())
			return [{
				"firestore_id": doc.id,
				**doc.to_dict()
			} for doc in docs]
		
		dados = await run_in_threadpool(fetch_data)
		logger.info(f"Encontrados {len(dados)} registros de sensores")
		return {
			"total": len(dados),
			"dados": dados
		}
	except Exception as e:
		logger.error(f"Erro inesperado ao buscar dados dos sensores: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Erro ao buscar dados dos sensores: {str(e)}")


@router.get("/dados/{id_compressor}")
async def get_compressor_data(
	id_compressor: int,
	limit: Optional[int] = Query(default=50, ge=1, le=1000, description="Número máximo de registros a retornar")
):
	"""Busca dados de um compressor específico."""
	logger.info(f"Buscando dados do sensor para compressor {id_compressor}")
	try:
		@handle_firestore_exceptions
		def fetch_compressor_data():
			# Buscar sem ordenação para evitar índice composto, depois ordenar em Python
			docs = list(
				db.collection("sensor_data")
				.where("id_compressor", "==", id_compressor)
				.limit(limit * 2)  # Buscar mais para compensar a ordenação local
				.stream()
			)
			# Ordenar por data_medicao em Python
			dados = [{
				"firestore_id": doc.id,
				**doc.to_dict()
			} for doc in docs]
			
			# Ordenar por data_medicao (mais recente primeiro)
			dados.sort(key=lambda x: x.get("data_medicao", ""), reverse=True)
			return dados[:limit]  # Aplicar limite após ordenação
		
		dados = await run_in_threadpool(fetch_compressor_data)
		
		if not dados:
			logger.warning(f"Nenhum dado encontrado para o compressor {id_compressor}")
			raise HTTPException(
				status_code=404, 
				detail=f"Nenhum dado encontrado para o compressor {id_compressor}"
			)
		
		logger.info(f"Encontrados {len(dados)} registros para o compressor {id_compressor}")
		return {
			"id_compressor": id_compressor,
			"total": len(dados),
			"dados": dados
		}
	except HTTPException:
		raise
	except Exception as e:
		logger.error(f"Erro inesperado ao buscar dados do compressor {id_compressor}: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Erro ao buscar dados do compressor: {str(e)}")


@router.get("/health")
async def health_check():
	"""Health check elaborado da aplicação."""
	logger.info("Health check solicitado")
	try:
		# Testar conexão com Firestore
		@handle_firestore_exceptions
		def test_firestore():
			# Teste simples de leitura
			docs = list(db.collection("compressores").limit(1).stream())
			return True
		
		firestore_ok = await run_in_threadpool(test_firestore)
		
		from ..utils.datetime_utils import now_br, format_br_datetime
		
		return {
			"status": "healthy",
			"timestamp": format_br_datetime(),
			"timezone": "America/Sao_Paulo (UTC-3)",
			"services": {
				"api": "online",
				"database": "online" if firestore_ok else "offline",
				"logging": "active"
			},
			"endpoints": {
				"compressores": "✅ CRUD completo",
				"sensores": "✅ Coleta de dados", 
				"health": "✅ Monitoramento"
			},
			"version": "1.0.0"
		}
	except Exception as e:
		logger.error(f"Erro no health check: {str(e)}")
		return {
			"status": "unhealthy",
			"timestamp": format_br_datetime(),
			"error": str(e),
			"services": {
				"api": "online",
				"database": "error",
				"logging": "active"
			}
		}


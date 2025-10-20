from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from ..models.sensor import SensorData, SensorOut, ESP32AlertasData, ESP32AlertasOut
from ..db.firebase import db
from ..utils.datetime_utils import now_br
from ..utils.error_handling import handle_firestore_exceptions
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


async def atualizar_status_compressor(id_compressor: int, esta_ligado: bool, data_medicao):
	"""Atualiza o status (ligado/desligado) de um compressor específico no Firestore."""
	try:
		@handle_firestore_exceptions
		def atualizar_status():
			# Buscar o compressor
			docs = list(db.collection("compressores").where("id_compressor", "==", id_compressor).limit(1).stream())
			if not docs:
				return False
			
			doc = docs[0]
			# Atualizar com o novo status e data da última atualização
			doc.reference.update({
				"esta_ligado": esta_ligado,
				"data_ultima_atualizacao": data_medicao
			})
			return True
		
		sucesso = await run_in_threadpool(atualizar_status)
		if sucesso:
			status_texto = "ligado" if esta_ligado else "desligado"
			logger.info(f"Status do compressor {id_compressor} atualizado para: {status_texto}")
		else:
			logger.warning(f"Compressor {id_compressor} não encontrado para atualizar status")
			
	except Exception as e:
		logger.error(f"Erro ao atualizar status do compressor {id_compressor}: {str(e)}")


@router.post("/sensor")
async def receive_sensor_data(data: SensorData):
	"""
	Recebe e armazena dados do sensor no Firestore.
	
	Parâmetros obrigatórios:
	- id_compressor: ID único do compressor
	- ligado: Status do compressor (ligado/desligado)
	- pressao: Pressão atual em bar (≥0)
	- temp_equipamento: Temperatura do equipamento em °C
	- temp_ambiente: Temperatura ambiente em °C
	- potencia_kw: Consumo de energia em kW (≥0)
	- umidade: Percentual de umidade (0-100%)
	- vibracao: Detecção de vibração anormal (true/false)
	- data_medicao: Data da medição (opcional, preenchida automaticamente)
	"""
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
		
		# Atualizar o status do compressor com o status do sensor
		await atualizar_status_compressor(data.id_compressor, data.ligado, data_dict["data_medicao"])
		
		status_texto = "ligado" if data.ligado else "desligado"
		logger.info(f"Dados do sensor salvos com sucesso (ID: {doc_id}), status do compressor atualizado para: {status_texto}")
	
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


@router.post("/esp32/alertas", response_model=ESP32AlertasOut)
async def update_esp32_alertas(data: ESP32AlertasData):
	"""
	Atualiza apenas os alertas do compressor baseado nos dados do ESP32.
	NÃO salva novos dados de medição, apenas atualiza os alertas no documento do compressor.
	
	Parâmetros obrigatórios:
	- id_compressor: ID único do compressor
	- alerta_potencia: Nível de alerta para potência
	- alerta_pressao: Nível de alerta para pressão
	- alerta_temperatura_ambiente: Nível de alerta para temperatura ambiente
	- alerta_temperatura_equipamento: Nível de alerta para temperatura equipamento
	- alerta_umidade: Nível de alerta para umidade
	- alerta_vibracao: Nível de alerta para vibração
	- data_medicao: Data da medição (opcional, preenchida automaticamente)
	"""
	logger.info(f"Atualizando alertas do ESP32 para compressor {data.id_compressor}")
	try:
		# Verificar se o compressor existe
		@handle_firestore_exceptions
		def verificar_compressor():
			docs = list(db.collection("compressores").where("id_compressor", "==", data.id_compressor).limit(1).stream())
			return len(docs) > 0
		
		compressor_existe = await run_in_threadpool(verificar_compressor)
		if not compressor_existe:
			logger.warning(f"Tentativa de atualizar alertas para compressor inexistente: {data.id_compressor}")
			raise HTTPException(
				status_code=404,
				detail=f"Compressor com ID {data.id_compressor} não encontrado. Cadastre o compressor primeiro."
			)
		
		# Preencher data_medicao se não foi informada
		data_medicao = data.data_medicao or now_br()
		
		# Organizar alertas do ESP32 para atualizar no compressor
		alertas_esp32 = {
			"potencia": data.alerta_potencia.value,
			"pressao": data.alerta_pressao.value,
			"temperatura_ambiente": data.alerta_temperatura_ambiente.value,
			"temperatura_equipamento": data.alerta_temperatura_equipamento.value,
			"umidade": data.alerta_umidade.value,
			"vibracao": data.alerta_vibracao.value
		}
		
		# Atualizar alertas do compressor com os dados do ESP32
		await atualizar_alertas_compressor(data.id_compressor, alertas_esp32)
		
		logger.info(f"Alertas do ESP32 atualizados com sucesso para compressor {data.id_compressor}: {alertas_esp32}")
	
		return ESP32AlertasOut(
			id_compressor=data.id_compressor,
			alertas_atualizados=alertas_esp32,
			data_atualizacao=data_medicao
		)
	except Exception as e:
		logger.error(f"Erro inesperado ao atualizar alertas do ESP32: {str(e)}")
		raise HTTPException(status_code=500, detail=f"Erro ao atualizar alertas do ESP32: {str(e)}")


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


from fastapi import APIRouter, HTTPException, Query
from fastapi.concurrency import run_in_threadpool
from ..models.compressor import CompressorData, CompressorOut, CompressorUpdate
from ..db.firebase import db
from ..utils.datetime_utils import now_br
from ..utils.error_handling import handle_firestore_exceptions, log_operation
from typing import List, Optional
import logging

logger = logging.getLogger(__name__)

router = APIRouter(tags=["compressores"], prefix="/compressores")


@router.post("/", response_model=dict)
async def criar_compressor(compressor: CompressorData):
    """Cria um novo compressor no sistema."""
    logger.info(f"Iniciando criação do compressor {compressor.id_compressor}")
    try:
        # Verificar se já existe um compressor com o mesmo ID
        @handle_firestore_exceptions
        def verificar_compressor_existente():
            existing = list(db.collection("compressores").where("id_compressor", "==", compressor.id_compressor).limit(1).stream())
            return len(existing) > 0
        
        existe = await run_in_threadpool(verificar_compressor_existente)
        if existe:
            raise HTTPException(
                status_code=400,
                detail=f"Já existe um compressor com ID '{compressor.id_compressor}'"
            )
        
        # Preparar dados para salvar
        compressor_dict = compressor.model_dump()
        compressor_dict["data_cadastro"] = now_br()
        
        # Salvar no Firestore
        @handle_firestore_exceptions
        def salvar_compressor():
            doc_ref = db.collection("compressores").add(compressor_dict)
            return doc_ref[1].id
        
        firestore_id = await run_in_threadpool(salvar_compressor)
        logger.info(f"Compressor {compressor.id_compressor} criado com sucesso (ID: {firestore_id})")
        
        return {
            "status": "sucesso",
            "message": "Compressor cadastrado com sucesso",
            "firestore_id": firestore_id,
            "id_compressor": compressor.id_compressor,
            "data_cadastro": compressor_dict["data_cadastro"]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao criar compressor {compressor.id_compressor}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao cadastrar compressor: {str(e)}")


@router.get("/", response_model=dict)
async def listar_compressores(
    ativo_apenas: Optional[bool] = Query(default=None, description="Filtrar apenas compressores ligados"),
    limit: Optional[int] = Query(default=50, ge=1, le=1000, description="Número máximo de registros")
):
    """Lista todos os compressores cadastrados."""
    logger.info(f"Listando compressores (ativo_apenas={ativo_apenas}, limit={limit})")
    try:
        @handle_firestore_exceptions
        def buscar_compressores():
            if ativo_apenas is not None:
                # Buscar apenas por filtro, sem ordenação para evitar índice composto
                docs = list(db.collection("compressores").where("esta_ligado", "==", ativo_apenas).limit(limit).stream())
            else:
                # Buscar todos, ordenados por timestamp
                docs = list(db.collection("compressores").order_by("data_cadastro", direction="DESCENDING").limit(limit).stream())
            
            return [{
                "firestore_id": doc.id,
                **doc.to_dict()
            } for doc in docs]
        
        compressores = await run_in_threadpool(buscar_compressores)
        logger.info(f"Encontrados {len(compressores)} compressores")
        
        return {
            "total": len(compressores),
            "compressores": compressores
        }
        
    except Exception as e:
        logger.error(f"Erro inesperado ao listar compressores: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar compressores: {str(e)}")


@router.get("/{id_compressor}", response_model=dict)
async def obter_compressor(id_compressor: int):
    """Obtém informações detalhadas de um compressor específico."""
    logger.info(f"Buscando compressor {id_compressor}")
    try:
        @handle_firestore_exceptions
        def buscar_compressor():
            docs = list(db.collection("compressores").where("id_compressor", "==", id_compressor).limit(1).stream())
            if not docs:
                return None
            doc = docs[0]
            return {
                "firestore_id": doc.id,
                **doc.to_dict()
            }
        
        compressor = await run_in_threadpool(buscar_compressor)
        
        if not compressor:
            logger.warning(f"Compressor {id_compressor} não encontrado")
            raise HTTPException(
                status_code=404,
                detail=f"Compressor com ID '{id_compressor}' não encontrado"
            )
        
        logger.info(f"Compressor {id_compressor} encontrado com sucesso")
        
        return {
            "compressor": compressor
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao buscar compressor {id_compressor}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao buscar compressor: {str(e)}")


@router.put("/{id_compressor}", response_model=dict)
async def atualizar_compressor(id_compressor: int, atualizacao: CompressorUpdate):
    """Atualiza informações de um compressor existente."""
    logger.info(f"Atualizando compressor {id_compressor}")
    try:
        # Buscar o compressor
        @handle_firestore_exceptions
        def buscar_e_atualizar():
            docs = list(db.collection("compressores").where("id_compressor", "==", id_compressor).limit(1).stream())
            if not docs:
                return None
            
            doc = docs[0]
            
            # Preparar dados para atualização (apenas campos não nulos)
            dados_atualizacao = {k: v for k, v in atualizacao.model_dump().items() if v is not None}
            
            if not dados_atualizacao:
                return "no_changes"
            
            dados_atualizacao["data_ultima_atualizacao"] = now_br()
            
            # Atualizar documento
            doc.reference.update(dados_atualizacao)
            
            # Retornar dados atualizados
            doc_atualizado = doc.reference.get()
            return {
                "firestore_id": doc_atualizado.id,
                **doc_atualizado.to_dict()
            }
        
        resultado = await run_in_threadpool(buscar_e_atualizar)
        
        if resultado is None:
            logger.warning(f"Compressor {id_compressor} não encontrado para atualização")
            raise HTTPException(
                status_code=404,
                detail=f"Compressor com ID '{id_compressor}' não encontrado"
            )
        
        if resultado == "no_changes":
            logger.warning(f"Nenhum campo válido fornecido para atualização do compressor {id_compressor}")
            raise HTTPException(
                status_code=400,
                detail="Nenhum campo válido fornecido para atualização"
            )
        
        logger.info(f"Compressor {id_compressor} atualizado com sucesso")
        
        return {
            "status": "sucesso",
            "message": "Compressor atualizado com sucesso",
            "compressor": resultado
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar compressor {id_compressor}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao atualizar compressor: {str(e)}")


@router.delete("/{id_compressor}", response_model=dict)
async def excluir_compressor(id_compressor: int):
    """Exclui um compressor do sistema."""
    logger.info(f"Excluindo compressor {id_compressor}")
    try:
        @handle_firestore_exceptions
        def buscar_e_excluir():
            docs = list(db.collection("compressores").where("id_compressor", "==", id_compressor).limit(1).stream())
            if not docs:
                return False
            
            doc = docs[0]
            doc.reference.delete()
            return True
        
        excluido = await run_in_threadpool(buscar_e_excluir)
        
        if not excluido:
            logger.warning(f"Compressor {id_compressor} não encontrado para exclusão")
            raise HTTPException(
                status_code=404,
                detail=f"Compressor com ID '{id_compressor}' não encontrado"
            )
        
        logger.info(f"Compressor {id_compressor} excluído com sucesso")
        
        return {
            "status": "sucesso",
            "message": f"Compressor '{id_compressor}' excluído com sucesso"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado ao excluir compressor {id_compressor}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Erro ao excluir compressor: {str(e)}")
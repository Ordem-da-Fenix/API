from fastapi import FastAPI
from .api.sensors import router as sensors_router
from .api.compressores import router as compressores_router
from .api.configuracoes import router as configuracoes_router
from .utils.error_handling import setup_logging

# Arquivo principal da aplicação dentro do pacote app.

# Configurar logging
setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(title="API - Ordem da Fenix - Monitoramento Industrial")
    
    # Incluir routers
    app.include_router(sensors_router)
    app.include_router(compressores_router)
    app.include_router(configuracoes_router)
    
    return app


app = create_app()

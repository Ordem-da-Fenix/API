from fastapi import FastAPI
from .api.sensors import router as sensors_router

# Arquivo principal da aplicação dentro do pacote app.

def create_app() -> FastAPI:
    app = FastAPI(title="API - Ordem da Fenix")
    
    # Incluir routers
    app.include_router(sensors_router)
    
    return app


app = create_app()

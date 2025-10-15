import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api.sensors import router as sensors_router
from .api.compressores import router as compressores_router
from .api.configuracoes import router as configuracoes_router
from .utils.error_handling import setup_logging

# Arquivo principal da aplicação dentro do pacote app.

# Configurar logging
setup_logging()

def create_app() -> FastAPI:
    app = FastAPI(
        title="API - Ordem da Fenix - Monitoramento Industrial",
        description="API para monitoramento de compressores industriais com sistema de alertas inteligente",
        version="1.0.0",
        docs_url="/docs" if os.getenv("ENVIRONMENT") != "production" else None,
        redoc_url="/redoc" if os.getenv("ENVIRONMENT") != "production" else None
    )
    
    # Configurar CORS - mais restritivo em produção
    allowed_origins = [
        "http://localhost:3000",           # React dev server
        "http://localhost:5500",           # Live Server (VS Code)
        "http://127.0.0.1:5500",          # Live Server (VS Code) - IP
        "http://localhost:8080",           # Vue/outros dev servers
        "http://127.0.0.1:8080",          # Vue/outros dev servers - IP
        "https://ordem-da-fenix.vercel.app",  # Frontend em produção (exemplo)
        "https://ordemdafenix.com.br",     # Domínio próprio (exemplo)
        "https://ordem-da-fenix.github.io", # Frontend estático GitHub Pages
    ]
    
    # Em desenvolvimento, permitir todas as origens
    if os.getenv("ENVIRONMENT") == "development":
        allowed_origins.append("*")
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        allow_headers=["*"],
    )
    
    # Rota de health check
    @app.get("/health")
    async def health_check():
        return {"status": "ok", "message": "API da Ordem da Fenix está funcionando!"}
    
    # Incluir routers
    app.include_router(sensors_router)
    app.include_router(compressores_router)
    app.include_router(configuracoes_router)
    
    return app


app = create_app()

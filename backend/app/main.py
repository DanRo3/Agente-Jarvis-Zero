# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importamos el motor y la Base de nuestros modelos para crear las tablas
from .db import models
from .db.database import engine

# Importamos el router de la API
from .api.routes import chat_routes, websocket_routes, auth_routes # ¡Añade websocket_routes!

# Esta línea crea las tablas en la base de datos si no existen.
# Para entornos de producción, se recomienda usar una herramienta de migración como Alembic.
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Agente IA Ultragenial - Backend",
    description="Backend para gestionar agentes de IA, conversaciones y más.",
    version="0.1.0",
)

# --- Configuración de CORS ---
# Esto es CRUCIAL para que tu frontend en localhost:5173 pueda hablar con el backend.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"], # El origen de tu app React
    allow_credentials=True,
    allow_methods=["*"], # Permitir todos los métodos (GET, POST, etc.)
    allow_headers=["*"], # Permitir todas las cabeceras
)

# --- Incluir Routers de la API ---
# Aquí es donde conectamos nuestras rutas modulares a la aplicación principal.
app.include_router(auth_routes.router)
app.include_router(chat_routes.router)
app.include_router(websocket_routes.router) # ¡Conecta el nuevo router!


# --- Ruta Raíz para Verificación ---
@app.get("/", tags=["Root"])
def read_root():
    return {"status": "El backend del agente de IA está funcionando correctamente"}

# El endpoint de WebSocket se moverá a su propio router en un paso futuro
# para mantener esta limpieza.
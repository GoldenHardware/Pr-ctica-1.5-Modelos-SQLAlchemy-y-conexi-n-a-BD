"""
Punto de entrada de la aplicación.

main.py solo crea y configura la app: no contiene rutas de negocio.
- core/middleware.py: CORS, tiempo de respuesta, request-id y log.
- core/errors.py: respuestas de error con formato común (422 y 500).
- core/database.py: engine, SessionLocal y get_db().
- models/: modelos SQLAlchemy (tablas).
- routers/: un router por recurso.
"""

from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.core.database import init_db
from app.core.config import API_V1_PREFIX, APP_DESCRIPTION, APP_NAME, APP_VERSION, TAGS_METADATA
from app.core.errors import register_exception_handlers
from app.core.logging import setup_logging
from app.core.middleware import register_middlewares
from app.routers import projects, system, tasks, users

setup_logging()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Al arrancar: crea las tablas en taskflow.db si no existen."""
    init_db()
    yield


app = FastAPI(
    title=APP_NAME,
    description=APP_DESCRIPTION,
    version=APP_VERSION,
    openapi_tags=TAGS_METADATA,
    lifespan=lifespan,
)

register_middlewares(app)
register_exception_handlers(app)

# Endpoints de sistema en la raíz (/health, /version, /ping)
app.include_router(system.router)

# Recursos de negocio versionados: /api/v1/users, /api/v1/projects, /api/v1/tasks
app.include_router(users.router, prefix=API_V1_PREFIX)
app.include_router(projects.router, prefix=API_V1_PREFIX)
app.include_router(tasks.router, prefix=API_V1_PREFIX)

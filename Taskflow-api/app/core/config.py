"""Configuración general de la API (un único sitio para cambiar nombre, versión, prefijo o CORS)."""

import os

APP_NAME = "TaskFlow API"
APP_VERSION = "0.5.0"
APP_DESCRIPTION = "API para gestionar proyectos y tareas (2ºDAW - Frameworks)."

# Entorno de ejecución: "development" (por defecto) o "production".
# Se cambia con la variable de entorno ENVIRONMENT.
ENVIRONMENT = os.getenv("ENVIRONMENT", "development")

# Prefijo común de los recursos de negocio. Si un día cambia el contrato,
# se crea /api/v2 sin romper a los clientes que usan /api/v1.
API_V1_PREFIX = "/api/v1"

# --- Base de datos -----------------------------------------------------------
# URL de conexión. Por defecto un archivo SQLite (taskflow.db) en la carpeta
# desde la que se arranca uvicorn. En otro entorno se cambia con la variable
# DATABASE_URL sin tocar el código, p. ej. PostgreSQL:
#   set DATABASE_URL=postgresql+psycopg://usuario:clave@localhost/taskflow
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./taskflow.db")

# Muestra en consola el SQL que genera SQLAlchemy (útil para aprender/depurar).
# Activado solo si SQL_ECHO=1.
SQL_ECHO = os.getenv("SQL_ECHO", "0") == "1"

# Segundos que espera una conexión SQLite si la BD está bloqueada por otra escritura.
DB_TIMEOUT = int(os.getenv("DB_TIMEOUT", "30"))

# --- CORS -------------------------------------------------------------------
# Orígenes (frontends) que pueden llamar a la API desde el navegador.
# En desarrollo es el servidor de Vite (http://localhost:5173). En producción
# se pasa la URL real con la variable CORS_ORIGINS, separando varias por comas:
#   set CORS_ORIGINS=https://taskflow.midominio.com
_DEFAULT_ORIGINS = {
    "development": "http://localhost:5173,http://127.0.0.1:5173",
    "production": "",  # en producción hay que indicarlo explícitamente
}
CORS_ORIGINS = [
    o.strip()
    for o in os.getenv("CORS_ORIGINS", _DEFAULT_ORIGINS.get(ENVIRONMENT, "")).split(",")
    if o.strip()
]

# Métodos y cabeceras que el frontend puede usar (solo los que la API necesita).
CORS_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
CORS_HEADERS = ["Content-Type", "Authorization", "X-Request-ID"]

# Cabeceras propias que el JavaScript del frontend puede LEER en la respuesta.
# Sin expose_headers el navegador las oculta aunque el servidor las envíe.
CORS_EXPOSE_HEADERS = ["X-Process-Time", "X-Request-ID"]

# Descripción de cada grupo (tag) que aparece en Swagger.
TAGS_METADATA = [
    {"name": "system", "description": "Comprobaciones del servidor: estado, versión y ping."},
    {"name": "users", "description": "Usuarios. Todos los usuarios comparten el mismo espacio de proyectos y tareas."},
    {"name": "projects", "description": "Gestión de **proyectos**. Un proyecto agrupa varias tareas."},
    {"name": "tasks", "description": "Gestión de **tareas**. Cada tarea pertenece a un proyecto (`project_id`)."},
]

"""Endpoints de sistema (no son de negocio): estado, versión, ping y prueba de errores."""

from fastapi import APIRouter

from app.core.config import APP_VERSION, ENVIRONMENT
from app.schemas import ErrorResponse

router = APIRouter(tags=["system"])


@router.get("/health", summary="Estado del servidor")
def health():
    return {"status": "ok"}


@router.get("/version", summary="Versión de la API")
def version():
    return {"version": APP_VERSION}


@router.get("/ping", summary="Comprobar que la API responde")
def ping():
    return {"message": "pong"}


@router.get(
    "/debug/error",
    summary="Forzar una excepción (solo desarrollo)",
    description=(
        "Lanza una excepción a propósito para comprobar el handler global: "
        "debe devolver 500 con `{\"error\": ...}` sin stacktrace y el servidor "
        "debe seguir funcionando. No está disponible en producción."
    ),
    responses={500: {"model": ErrorResponse, "description": "Error interno"}},
    include_in_schema=ENVIRONMENT != "production",
)
def force_error():
    if ENVIRONMENT == "production":
        return {"message": "No disponible en producción"}
    # Error típico de programación: división entre cero.
    return {"resultado": 1 / 0}

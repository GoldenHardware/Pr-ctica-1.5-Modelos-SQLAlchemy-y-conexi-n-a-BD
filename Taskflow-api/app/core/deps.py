"""
Dependencias reutilizables de FastAPI.

get_current_user es una dependencia ANIDADA: depende a su vez de get_db.
FastAPI resuelve primero get_db (abre la sesión), se la pasa a
get_current_user y, si un endpoint pide las dos, reutiliza la MISMA sesión
dentro de la petición (FastAPI cachea cada dependencia por petición).
"""

from typing import Annotated

from fastapi import Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models import User

# Alias para no repetir "Session = Depends(get_db)" en cada endpoint.
DbSession = Annotated[Session, Depends(get_db)]


def get_current_user(
    db: DbSession,
    x_user_id: Annotated[int | None, Header(description="Id del usuario (temporal, hasta tener login).")] = None,
) -> User:
    """
    Usuario que hace la petición. TEMPORAL: lo identifica por la cabecera
    X-User-ID. Cuando haya autenticación se sustituirá por la lectura del token,
    sin cambiar los endpoints que la usan.
    """
    if x_user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Falta la cabecera X-User-ID")
    user = db.get(User, x_user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuario no válido")
    return user


CurrentUser = Annotated[User, Depends(get_current_user)]

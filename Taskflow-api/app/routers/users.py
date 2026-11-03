"""Router del recurso /users."""

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.core.deps import CurrentUser, DbSession
from app.core.security import hash_password
from app.models import User
from app.schemas import ErrorResponse, UserCreate, UserRead

router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={422: {"model": ErrorResponse, "description": "Datos no válidos"}},
)


@router.post(
    "",
    response_model=UserRead,
    status_code=status.HTTP_201_CREATED,
    summary="Registrar un usuario",
    responses={409: {"model": ErrorResponse, "description": "Nombre de usuario ya existente"}},
)
def create_user(data: UserCreate, db: DbSession):
    if db.scalar(select(User).where(User.username == data.username)):
        # RF-02: rechazar un nombre de usuario repetido informando del motivo.
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El nombre de usuario ya existe")
    user = User(username=data.username, hashed_password=hash_password(data.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.get(
    "/me",
    response_model=UserRead,
    summary="Usuario actual",
    description="Devuelve el usuario de la cabecera `X-User-ID` (ejemplo de dependencia anidada get_current_user → get_db).",
    responses={401: {"model": ErrorResponse, "description": "Sin usuario o usuario no válido"}},
)
def read_me(current_user: CurrentUser):
    return current_user

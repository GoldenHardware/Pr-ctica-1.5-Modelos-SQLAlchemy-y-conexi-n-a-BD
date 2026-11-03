"""Schemas del recurso Usuario."""

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.common import SchemaBase


class UserCreate(SchemaBase):
    """Registro de usuario (RF-01): nombre de usuario y contraseña."""

    username: str = Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_]+$",
                          description="Nombre de usuario (3-50, letras, números y _).")
    password: str = Field(min_length=8, max_length=128, description="Contraseña (mín. 8 caracteres).")

    model_config = ConfigDict(json_schema_extra={"examples": [{"username": "duro", "password": "secreto123"}]})


class UserRead(BaseModel):
    """Usuario devuelto por la API. Nunca incluye la contraseña ni su hash."""

    id: int
    username: str

    model_config = ConfigDict(from_attributes=True)

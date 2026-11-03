"""Schemas Pydantic: el contrato de entrada/salida de la API, separado por recurso."""

from app.schemas.common import ErrorResponse, FieldError, SchemaBase
from app.schemas.project import ProjectCreate, ProjectRead
from app.schemas.task import TaskCreate, TaskRead
from app.schemas.user import UserCreate, UserRead

__all__ = [
    "SchemaBase", "FieldError", "ErrorResponse",
    "ProjectCreate", "ProjectRead",
    "TaskCreate", "TaskRead",
    "UserCreate", "UserRead",
]

"""Schemas del recurso Proyecto."""

from datetime import datetime

from pydantic import ConfigDict, Field

from app.schemas.common import SchemaBase


class ProjectBase(SchemaBase):
    """Campos comunes de un proyecto."""

    name: str = Field(min_length=1, max_length=100, description="Nombre del proyecto (1-100 caracteres).")
    description: str | None = Field(
        default=None, max_length=500, description="Descripción opcional (máx. 500 caracteres)."
    )


class ProjectCreate(ProjectBase):
    """Datos que envía el cliente para crear un proyecto."""

    model_config = ConfigDict(
        json_schema_extra={"examples": [{"name": "TaskFlow", "description": "Gestor de tareas de 2ºDAW"}]}
    )


class ProjectRead(ProjectBase):
    """Proyecto tal y como lo devuelve la API."""

    id: int = Field(description="Identificador único generado por el servidor.")
    created_at: datetime = Field(description="Fecha y hora de creación.")

    model_config = ConfigDict(
        from_attributes=True,
        extra="ignore",
        json_schema_extra={
            "examples": [
                {
                    "id": 1,
                    "name": "TaskFlow",
                    "description": "Gestor de tareas de 2ºDAW",
                    "created_at": "2026-11-03T18:00:00",
                }
            ]
        },
    )

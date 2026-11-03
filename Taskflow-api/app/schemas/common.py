"""Schemas compartidos por todos los recursos."""

from pydantic import BaseModel, ConfigDict, Field


class SchemaBase(BaseModel):
    """Configuración común a todos los schemas de entrada."""

    model_config = ConfigDict(
        str_strip_whitespace=True,  # "   " se convierte en "" y falla min_length
        extra="forbid",             # rechaza campos que no existen en el schema
    )


class FieldError(BaseModel):
    """Un error concreto de validación."""

    campo: str = Field(description="Campo que ha fallado, p. ej. 'title'.")
    mensaje: str = Field(description="Explicación legible del error.")


class ErrorResponse(BaseModel):
    """Formato común de todas las respuestas de error de la API."""

    error: str = Field(description="Mensaje legible para el cliente.")
    error_code: str = Field(description="Código estable del error, p. ej. VALIDATION_ERROR o INTERNAL_ERROR.")
    request_id: str | None = Field(default=None, description="Id de la petición, para buscarla en los logs.")
    errors: list[FieldError] | None = Field(default=None, description="Errores por campo (solo en 422).")

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "error": "Error de validación en los datos enviados",
                    "error_code": "VALIDATION_ERROR",
                    "request_id": "3f2a9c1e8b7d4e6f9a0b1c2d3e4f5a6b",
                    "errors": [{"campo": "title", "mensaje": "Debe tener al menos 1 carácter(es)"}],
                }
            ]
        }
    )

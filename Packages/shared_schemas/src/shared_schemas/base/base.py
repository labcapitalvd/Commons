from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_snake


##############################################################################################
# Base
##############################################################################################
class BaseSchema(BaseModel):
    """Modelo base para todas las clases de esquema."""

    model_config = ConfigDict(
        validate_by_name=True,
        alias_generator=to_snake,
    )


##############################################################################################
# ID
##############################################################################################
class UuidSchema(BaseSchema):
    """Modelo para representar un UUID."""

    id: UUID = Field(
        ...,
        title="UUID del objeto.",
        description="el UUID en v4 o v7 de un objeto en la db"
    )


##############################################################################################
# Message
##############################################################################################
class ResponseMessage(BaseSchema):
    """Modelo para representar un mensaje de respuesta."""

    message: str = Field(
        ...,
        min_length=1,
        max_length=256,
        title="Mensaje de API.",
        description="Un mensaje personalizable de la API.",
    )

from pydantic import Field

from shared_schemas import (
    BaseSchema,
    Username,
    UserEmail,
    UserPassword,
)

##############################################################################################
# Requests
##############################################################################################


class RequestRegister(Username, UserEmail, UserPassword):
    """Request body for registering a new user."""


class RequestLogin(Username, UserPassword):
    """Request body for logging in a user."""


class RefreshTokenBody(BaseSchema):
    refresh_token: str


##############################################################################################
# Responses
##############################################################################################


class ResponseRegister(Username, UserEmail):
    """Modelo para representar un registro."""

    message: str = Field(
        default="Registro correcto",
        min_length=2,
        max_length=256,
        description="Un mensaje que indica que el registro fue exitoso.",
    )


class ResponseDelete(Username, UserEmail):
    """Modelo para representar un delete."""

    message: str = Field(
        default="Delete correcto",
        min_length=2,
        max_length=256,
        description="Un mensaje que indica que el delete fue exitoso.",
    )


class ResponseLogout(BaseSchema):
    """Modelo para representar un logout."""

    message: str = Field(
        default="Logout correcto",
        min_length=2,
        max_length=256,
        description="Un mensaje que indica que el logout fue exitoso.",
    )


class ResponseUpdate(BaseSchema):
    """Modelo para representar un update."""

    message: str = Field(
        default="Usuario actualizado correctamente",
        min_length=2,
        max_length=256,
        description="Un mensaje que indica que el update fue exitoso.",
    )

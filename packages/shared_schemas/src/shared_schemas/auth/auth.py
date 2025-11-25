from shared_schemas import BaseSchema
from pydantic import Field, EmailStr, SecretStr

##############################################################################################
# Auth
##############################################################################################


class Username(BaseSchema):
    """Request body for registering a new user."""

    username: str = Field(
        ..., min_length=4, max_length=128, description="Nombre de usuario"
    )


class UserEmail(BaseSchema):
    """Request body for registering a new user."""

    email: EmailStr = Field(
        ..., min_length=8, max_length=256, description="Correo electrónico válido"
    )


class UserPassword(BaseSchema):
    """Request body for registering a new user."""

    password: SecretStr = Field(
        ..., min_length=8, max_length=128, description="Contraseña del usuario"
    )


class Platform(BaseSchema):
    """Platform from which the user is accessing the application."""

    platform: str = Field(
        default="web",
        min_length=3,
        max_length=10,
        description="Platform: 'web' or 'mobile'",
    )


class AccessToken(BaseSchema):
    """Modelo para representar un token de acceso."""

    access_token: str = Field(
        ..., min_length=36, max_length=512, description="Token de acceso."
    )
    token_type: str = Field(
        default="bearer", min_length=2, max_length=128, description="Tipo de token"
    )


class RefreshToken(BaseSchema):
    """Modelo para representar un token de refresco."""

    refresh_token: str = Field(
        ..., min_length=36, max_length=512, description="Token de refresco."
    )
    token_type: str = Field(
        default="bearer", min_length=2, max_length=128, description="Tipo de token"
    )


class ResponseWeb(AccessToken):
    """Response from a reauth endpoint."""

    message: str = Field(
        default="Auth correcto en web.",
        min_length=2,
        max_length=256,
        description="Indica que el reauth fue exitoso en web.",
    )


class ResponseMobile(AccessToken, RefreshToken):
    """Response from a reauth endpoint."""

    message: str = Field(
        default="Auth correcto en móvil.",
        min_length=2,
        max_length=256,
        description="Indica que el reauth fue exitoso en móvil.",
    )

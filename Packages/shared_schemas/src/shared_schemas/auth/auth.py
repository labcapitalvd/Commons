from shared_schemas import BaseSchema
from pydantic import Field, EmailStr, SecretStr

##############################################################################################
# Auth
##############################################################################################


class Username(BaseSchema):
    """Request body for registering a new user."""
    username: str = Field(
        ..., 
        min_length=4, 
        max_length=128, 
        title="Username",
        description="Nombre de usuario"
    )


class UserEmail(BaseSchema):
    """Request body for registering a new user."""
    email: EmailStr = Field(
        ..., 
        min_length=8, 
        max_length=256, 
        title="Email",
        description="Correo electrónico válido"
    )


class UserPassword(BaseSchema):
    """Request body for registering a new user."""
    password: SecretStr = Field(
        ..., 
        min_length=8, 
        max_length=128, 
        title="Password",
        description="Contraseña del usuario"
    )


class Platform(BaseSchema):
    """Platform from which the user is accessing the application."""
    platform: str = Field(
        default="web",
        min_length=3,
        max_length=10,
        title="Platform",
        description="Platform: 'web' o 'mobil. Web usa cookies, Web guarda cookie, mobile espera almacenamiento seguro de refresh por cliente'",
    )


class BaseToken(BaseSchema):
    """Modelo para representar un token genérico."""
    token_type: str = Field(
        default="bearer", 
        min_length=2, 
        max_length=128, 
        title="Type",
        description="Tipo de token"
    )


class AccessToken(BaseToken):
    """Modelo para representar un token de acceso."""
    access_token: str = Field(
        ..., 
        min_length=36, 
        max_length=512, 
        title="Access token",
        description="Token de acceso."
    )

class RefreshToken(BaseToken):
    """Modelo para representar un token de refresco."""
    refresh_token: str = Field(
        ..., 
        min_length=36, 
        max_length=512, 
        title="Refresh token",
        description="Token de refresco."
    )


class ResponseWeb(AccessToken):
    """Response from a reauth endpoint."""
    message: str = Field(
        default="Auth correcto en web.",
        min_length=2,
        max_length=256,
        title="WebAuth",
        description="Indica que el reauth fue exitoso en web.",
    )


class ResponseMobile(AccessToken, RefreshToken):
    """Response from a reauth endpoint."""
    message: str = Field(
        min_length=2,
        max_length=256,
        title="MobileAuth",
        description="Indica que el reauth fue exitoso en móvil.",
    )

from pydantic import EmailStr, SecretStr, field_validator

from shared_utils import TextUtils
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
    
    
    @field_validator("username")
    @classmethod
    def validate_username(cls, v: str) -> str:
        return TextUtils.sanitize_text(v)

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: EmailStr) -> str:
        return TextUtils.is_valid_and_safe_email(v)

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> str:
        return TextUtils.sanitize_text(v.get_secret_value())



class RequestLogin(Username, UserPassword):
    """Request body for logging in a user."""


class RefreshTokenBody(BaseSchema):
    refresh_token: str


##############################################################################################
# Responses
##############################################################################################


from typing import Annotated, Union

from pydantic import SecretStr

from fastapi import APIRouter, Depends, Form, HTTPException, status
from fastapi.security import OAuth2PasswordRequestFormStrict

from sqlalchemy.ext.asyncio import AsyncSession

from application import AuthAppService
from domain import AuthService, TokenService

from schemas.auth import RequestRegister
from schemas.auth import ResponseRegister, ResponseLogout

from shared_db import get_session
from shared_schemas import ResponseWeb, ResponseMobile, ResponseMessage
from shared_utils import TokenContext
from shared_utils.tokens.tokens import get_refresh_token

class UserAlreadyExists(Exception):
    """Usuario ya existe."""

router = APIRouter(tags=["Autenticación"], prefix="/auth")


@router.post(
    "/register",
    response_model=ResponseMessage,
    response_model_exclude_none=True,
    operation_id="register_user",
)
async def register(
    form: Annotated[RequestRegister, Form()],
):
    """Function for registering"""
    try:
        auth_service = AuthService()
        user = await auth_service.register(
            form.username, 
            form.email, 
            form.password.get_secret_value()
        )
        return ResponseMessage(message="correct")
    except UserAlreadyExists:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Registration failed: {str(e)}"
        )



@router.post(
    "/login",
    response_model=Union[ResponseWeb, ResponseMobile],
    response_model_exclude_none=True,
    operation_id="login_user",
)
async def login(
    form_data: OAuth2PasswordRequestFormStrict = Depends(),
    ctx: TokenContext = Depends(),
):
    """Function for logging in"""
    password = SecretStr(form_data.password)
    auth_service = AuthService()
    token_service = TokenService()
    access_token, refresh_token = await AuthAppService(auth_service, token_service).login_and_issue_tokens(
        form_data.username, password.get_secret_value()
    )
    return ctx.make_return(access_token, refresh_token)


@router.post(
    "/reauth",
    response_model=Union[ResponseWeb, ResponseMobile],
    response_model_exclude_none=True,
    operation_id="reauth_user",
)
async def refresh_token(
    refresh_token: str = Depends(get_refresh_token),
    ctx: TokenContext = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """Function for refreshing token"""
    tokens = await AuthService(db).rotate_tokens(refresh_token)
    return ctx.make_return(*tokens)


@router.post(
    "/logout",
    response_model=ResponseLogout,
    response_model_exclude_none=True,
    operation_id="logout_user",
)
async def logout(
    refresh_token: str = Depends(get_refresh_token),
    ctx: TokenContext = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """Function for logging out"""
    await AuthService(db).logout_user(refresh_token)
    return ResponseLogout()

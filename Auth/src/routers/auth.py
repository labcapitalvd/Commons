from typing import Annotated, Union

from pydantic import SecretStr

from fastapi import APIRouter, Depends, Form, HTTPException
from fastapi.security import OAuth2PasswordRequestFormStrict

from sqlalchemy.ext.asyncio import AsyncSession

from application import AuthAppService
from schemas.auth import RequestRegister


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
        await AuthAppService().register(
            form.username,
            form.email,
            form.password.get_secret_value(),
        )
        return ResponseMessage(message="correct")

    except UserAlreadyExists:
        raise HTTPException(status_code=400, detail="User already exists")



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
    access_token, refresh_token = await AuthAppService().login_and_issue_tokens(
        username=form_data.username,
        password=password.get_secret_value()
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
    tokens = await AuthAppService().reauth_refresh(
        old_refresh_token=refresh_token
    )
    return ctx.make_return(*tokens)


@router.post(
    "/logout",
    response_model=ResponseMessage,
    response_model_exclude_none=True,
    operation_id="logout_user",
)
async def logout(
    refresh_token: str = Depends(get_refresh_token),
    ctx: TokenContext = Depends(),
    db: AsyncSession = Depends(get_session),
):
    """Function for logging out"""
    await AuthAppService().logout(
        refresh_token=refresh_token
    )
    return ResponseMessage(message="ok")

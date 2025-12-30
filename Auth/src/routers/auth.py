from typing import Annotated, Union

from pydantic import SecretStr

from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordRequestFormStrict

from sqlalchemy.ext.asyncio import AsyncSession

from handlers.users import UserHandler
from services.auth import AuthService
from schemas.auth import RequestRegister
from schemas.auth import ResponseRegister, ResponseLogout

from shared_db import get_session
from shared_schemas import ResponseWeb, ResponseMobile
from shared_schemas import CustomError, ItemError
from shared_utils.auth.auth import TokenContext, get_refresh_token

router = APIRouter(tags=["Autenticación"], prefix="/auth")


@router.post(
    "/register",
    response_model=ResponseRegister,
    response_model_exclude_none=True,
    operation_id="register_user",
)
async def register(
    form: Annotated[RequestRegister, Form()],
    db: AsyncSession = Depends(get_session),
):
    """Function for registering"""
    try:
        user = await UserHandler(db).register_user(
            form.username, form.email, form.password
        )

        if user:
            return ResponseRegister(username=user.username, email=user.email)
        else:
            raise CustomError(
                errors=[
                    ItemError(
                        code="USER_ALREADY_EXISTS",
                        message="Registration failed on router.",
                        more_info="User already exists.",
                    )
                ]
            )

    except Exception as e:
        raise CustomError(
            errors=[
                ItemError(
                    code="REGISTRATION_FAILED_ROUTER",
                    message="Registration failed on router.",
                    more_info=str(e),
                )
            ]
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
    db: AsyncSession = Depends(get_session),
):
    """Function for logging in"""
    password = SecretStr(form_data.password)
    access_token, refresh_token = await AuthService(db).login_with_tokens(
        form_data.username, password
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

from typing import Sequence, Annotated
from annotated_types import Len
from pydantic import Field

from fastapi import FastAPI, APIRouter, HTTPException, Request
from fastapi.routing import APIRoute
from fastapi.responses import JSONResponse

from shared_schemas import BaseSchema


class ItemError(BaseSchema):
    """Modelo que representa un error de validación."""

    code: str = Field(
        ..., min_length=1, max_length=512, description="Error code identifier"
    )
    message: str = Field(
        ..., min_length=1, max_length=512, description="Human-readable error message"
    )
    more_info: str = Field(
        ..., min_length=1, max_length=512, description="Additional info about the error"
    )


class ResponseError(BaseSchema):
    """Modelo que representa una respuesta de error de validación."""

    errors: Annotated[list[ItemError], Len(min_length=1, max_length=512)] = Field(
        ..., description="Lista de errores"
    )

    trace: str = Field(
        ..., min_length=1, max_length=512, description="Trace of the validation failure"
    )



class CustomError(HTTPException):
    def __init__(self, errors: Sequence[ItemError], trace: str = "Custom error raised"):
        """
        Only accept ItemError instances.
        """
        super().__init__(
            status_code=400,
            detail={"errors": [e.model_dump() for e in errors], "trace": trace},
        )


async def custom_error_handler(request: Request, exc: Exception):
    """
    Returns your CustomError in Orval-compatible format.
    """
    if isinstance(exc, CustomError):
        return JSONResponse(status_code=exc.status_code, content=exc.detail)

    # fallback for other exceptions
    return JSONResponse(
        status_code=500,
        content={
            "errors": [
                {"code": "INTERNAL_ERROR", "message": str(exc), "more_info": ""}
            ],
            "trace": "Unexpected exception",
        },
    )


def add_custom_error_responses(router: APIRouter):
    """
    Automatically add 400 ResponseError to all routes in the router.
    Merges with existing responses if they exist.
    """
    for route in router.routes:
        if isinstance(route, APIRoute):
            # ensure the responses dict exists
            route.responses = route.responses or {}

            # only add 400 if not already present
            if 400 not in route.responses:
                route.responses[400] = {"model": ResponseError}
            if 422 not in route.responses:
                route.responses[422] = {"model": ResponseError}
    return router


def add_routers_with_custom_errors(app: FastAPI, routers: list[APIRouter]):
    """
    Include multiple routers and automatically annotate all endpoints with 400 ResponseError
    """
    for router in routers:
        router = add_custom_error_responses(router)
        app.include_router(router)

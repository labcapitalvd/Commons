from fastapi import Request
from fastapi.responses import JSONResponse

from domain.services.auth.errors import UserAlreadyExists, InvalidCredentials, TierDoesntExist

async def auth_exception_handler(request: Request, exc: Exception):
    if isinstance(exc, UserAlreadyExists):
        return JSONResponse(
            status_code=409,  # Conflict
            content={"success": False, "error": "User already exists"}
        )
    elif isinstance(exc, InvalidCredentials):
        return JSONResponse(
            status_code=401,  # Unauthorized
            content={"success": False, "error": "Invalid credentials"}
        )
    elif isinstance(exc, TierDoesntExist):
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": "Default tier not found"}
        )
    # fallback
    return JSONResponse(
        status_code=500,
        content={"success": False, "error": "Internal server error"}
    )

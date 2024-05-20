from domain.ecommerce.exceptions.exceptions import (
    UnauthorizedException,
    UserNotFoundException,
)
from domain.ecommerce.use_case.auth import (
    get_current_active_buyer_logic,
    get_current_user_logic,
    reset_password_logic,
    forgot_password_logic,
    login_logic,
    get_current_active_dealer_logic,
)

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import JSONResponse

from infrastructure.api.dto.dto_auth import Login

router = APIRouter()


@router.post("/login")
async def login(login_data: Login) -> JSONResponse:
    try:
        response = await login_logic(login_data)
        return response
    except UnauthorizedException as e:
        raise HTTPException(status_code=401, detail=str(e))


@router.post("/forgot_password")
async def forgot_password(email: str):
    try:
        response = await forgot_password_logic(email)
        return response
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/reset_password")
async def reset_password(user_id: int, new_password: str):
    try:
        response = await reset_password_logic(user_id, new_password)
        return response
    except UserNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

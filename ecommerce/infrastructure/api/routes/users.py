from domain.ecommerce.use_case.auth import get_current_user_logic
from domain.ecommerce.use_case.users import (
    get_users_logic,
    create_user_logic,
    confirm_user_logic,
    update_user_logic,
    delete_user_logic,
)
from fastapi import APIRouter, Depends, HTTPException

from infrastructure.api.dto.dto_user import UserRequest, UserResponse, UserUpdate

router = APIRouter()


@router.get("/users")
async def get_users(role: str = None):  # type: ignore
    return await get_users_logic(role)


@router.post("/create_users")
async def create_user(user_data: UserRequest):
    return await create_user_logic(user_data)


@router.get("/confirm/{user_id}")
async def confirm_user(user_id: str):
    return await confirm_user_logic(user_id)


@router.put(
    "/update_profile",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user_logic)],
)
async def update_user(user_data: UserUpdate):
    return await update_user_logic(user_data)


@router.delete("/delete_profile", dependencies=[Depends(get_current_user_logic)])
async def delete_user():
    return await delete_user_logic()

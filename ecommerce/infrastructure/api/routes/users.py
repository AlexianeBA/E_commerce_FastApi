from typing import Optional
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
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
async def get_users(role: Optional[str] = None):
    try:
        return await get_users_logic(role)
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/create_users")
async def create_user(user_data: UserRequest):
    try:
        return await create_user_logic(user_data)
    except UserAlreadyExistsException as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/confirm/{user_id}")
async def confirm_user(user_id: str):
    try:
        return await confirm_user_logic(user_id)
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put(
    "/update_profile",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user_logic)],
)
async def update_user(user_data: UserUpdate):
    try:
        return await update_user_logic(user_data)
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/delete_profile", dependencies=[Depends(get_current_user_logic)])
async def delete_user():
    try:
        return await delete_user_logic()
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

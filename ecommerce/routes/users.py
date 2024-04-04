from typing import List
from fastapi import APIRouter, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import UserUpdate, UserResponse, UserRequest
from tables import User
from settings import pwd_context

router = APIRouter()


@router.get("/users", response_model=List[UserResponse])
async def get_users():
    users = await User.select().run()
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "password": user["password"],
            "is_buyer": user["is_buyer"],
            "is_dealer": user["is_dealer"],
        }
        for user in users
    ]


@router.post("/users/", response_model=UserResponse)
async def create_user(user_data: UserRequest):
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        is_superuser=user_data.is_superuser,
        is_staff=user_data.is_staff,
        is_active=user_data.is_active,
        is_buyer=user_data.is_buyer,
        is_dealer=user_data.is_dealer,
        date_joined=user_data.date_joined,
    )
    await user.save().run()
    return UserResponse(**user.to_dict())


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user_data: UserUpdate) -> JSONResponse:
    user = await User.objects().where(User.id == user_id).first().run()
    if user:
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.password is not None:
            user.password = pwd_context.hash(user_data.password)
        if user_data.first_name is not None:
            user.first_name = user_data.first_name
        if user_data.last_name is not None:
            user.last_name = user_data.last_name
        if user_data.email is not None:
            user.email = user_data.email
        await user.save().run()
        # return UserResponse(**user.to_dict())
    log_dict = {
        "code": "200",
        "type": "",
        "message": "utilisateur modifié avec succés",
    }
    json_compatible_item_data = jsonable_encoder(log_dict)
    return JSONResponse(
        content=json_compatible_item_data,
        status_code=status.HTTP_200_OK,
    )


@router.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = await User.objects().where(User.id == user_id).first().run()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.remove().run()
    return {"message": "User deleted"}

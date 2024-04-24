from typing import List
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ecommerce.models.user_models import UserUpdate, UserResponse, UserRequest
from ecommerce.tables import User
from ecommerce.settings import pwd_context
from ecommerce.routes.auth import get_current_user

router = APIRouter()


@router.get(
    "/users",
    response_model=List[UserResponse],
)
async def get_users() -> JSONResponse:
    users = await User.select().run()
    return JSONResponse(
        [
            {
                "message": "Liste de tous les utilisateurs:",
                "id": user["id"],
                "username": user["username"],
                "password": user["password"],
                "role": user["role"],
            }
            for user in users
        ]
    )


@router.post("/create_users/", response_model=UserResponse)
async def create_user(user_data: UserRequest) -> JSONResponse:
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
        role=user_data.role,
    )
    await user.save().run()
    return JSONResponse(content=user.to_dict(), status_code=status.HTTP_200_OK)


@router.put(
    "/update_profile",
    response_model=UserResponse,
    dependencies=[Depends(get_current_user)],
)
async def update_user(
    user_data: UserUpdate, current_user=Depends(get_current_user)
) -> JSONResponse:
    user = await User.objects().where(User.id == current_user.id).first().run()
    if user:
        if user_data.username is not None:
            user.username = user_data.username
        if user_data.password is not None:
            user.password = pwd_context.hash(user_data.password)
        if user_data.name is not None:
            user.name = user_data.name
        if user_data.email is not None:
            user.email = user_data.email
        await user.save().run()

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


@router.delete("/delete_profile", dependencies=[Depends(get_current_user)])
async def delete_user(current_user=Depends(get_current_user)) -> JSONResponse:
    user = await User.objects().where(User.id == current_user.id).first().run()
    if user:
        await user.remove().run()
        return JSONResponse({"message": "Profil supprimé avec succès"})

    else:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

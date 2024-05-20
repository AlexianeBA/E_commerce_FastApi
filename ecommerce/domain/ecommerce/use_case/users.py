from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import (
    UserAlreadyExistsException,
    UserNotFoundException,
)
from infrastructure.api.dto.dto_user import UserUpdate, UserRequest

from models.users_models import User
from settings import pwd_context
from domain.ecommerce.use_case.auth import get_current_user_logic


async def get_users_logic(role: Optional[str] = None) -> JSONResponse:
    try:
        if role:
            users = await User.objects().where(User.role == role).run()
        else:
            users = await User.select().run()

        if not users:
            raise UserNotFoundException("Aucun utilisateur trouvé")

        return JSONResponse(
            [
                {
                    "id": user["id"],
                    "username": user["username"],
                    "password": user["password"],
                    "role": user["role"],
                }
                for user in users
            ]
        )
    except UserNotFoundException as e:
        return JSONResponse(status_code=404, content={"message": str(e)})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


async def create_user_logic(user_data: UserRequest) -> JSONResponse:
    existing_user = (
        await User.objects().where(User.username == user_data.username).first().run()
    )
    if existing_user is not None:
        raise UserAlreadyExistsException(
            "Un utilisateur avec ce nom d'utilisateur existe déjà"
        )

    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        name=user_data.name,
        email=user_data.email,
        date_of_birth=user_data.date_of_birth,
        gender=user_data.gender,
        location=user_data.location,
        role=user_data.role,
    )
    await user.save().run()

    return JSONResponse(
        content={
            "id": user.id,
            "username": user.username,
            "password": user.password,
            "role": user.role,
        },
        status_code=201,
    )


async def confirm_user_logic(user_id: str):
    user = await User.objects().where(User.id == user_id).first().run()
    if user:
        user.is_active = True
        await user.save().run()
        return JSONResponse({"message": "User confirmed successfully"})
    else:
        raise UserNotFoundException("User not found")


async def update_user_logic(
    user_data: UserUpdate, current_user=Depends(get_current_user_logic)
) -> JSONResponse:
    user = await User.objects().where(User.id == current_user.id).first().run()
    if user is None:
        raise UserNotFoundException("User not found")

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


async def delete_user_logic(
    current_user=Depends(get_current_user_logic),
) -> JSONResponse:
    user = await User.objects().where(User.id == current_user.id).first().run()
    if user:
        await user.remove().run()
        return JSONResponse({"message": "Profil supprimé avec succès"})
    else:
        raise UserNotFoundException("Utilisateur non trouvé")

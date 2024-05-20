from typing import List, Optional
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from infrastructure.api.dto.dto_user import UserUpdate, UserResponse, UserRequest
from infrastructure.api.dto.dto_smtp import EmailRequest
from domain.ecommerce.models.users_models import User
from settings import pwd_context
from domain.ecommerce.use_case.auth import get_current_user_logic
from domain.ecommerce.use_case.smtp import send_email_logic


async def get_users_logic(role: Optional[str] = None) -> JSONResponse:
    if role:
        users = await User.objects().where(User.role == role).run()
    else:
        users = await User.select().run()
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


async def create_user_logic(user_data: UserRequest) -> JSONResponse:
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
    confirmation_url = f"http://localhost:8000/docs#/users/confirm_user_confirm__user_id__get/{user.id}"
    await user.save().run()
    email_request = EmailRequest(
        receiver_email=user.email,
        subject="Please confirm your account",
        body=f"Welcome {user.username}, please confirm your account by clicking on the following URL: {confirmation_url}",
    )
    await send_email_logic(email_request)
    return JSONResponse(content=user.to_dict(), status_code=status.HTTP_200_OK)


async def confirm_user_logic(user_id: str):
    user = await User.objects().where(User.id == user_id).first().run()
    if user:
        user.is_active = True
        await user.save().run()
        return JSONResponse({"message": "User confirmed successfully"})
    else:
        raise HTTPException(status_code=404, detail="User not found")


async def update_user_logic(
    user_data: UserUpdate, current_user=Depends(get_current_user_logic)
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


async def delete_user_logic(
    current_user=Depends(get_current_user_logic),
) -> JSONResponse:
    user = await User.objects().where(User.id == current_user.id).first().run()
    if user:
        await user.remove().run()
        return JSONResponse({"message": "Profil supprimé avec succès"})

    else:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")

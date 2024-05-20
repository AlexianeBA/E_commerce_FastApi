from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt as jwt
from infrastructure.api.dto.dto_auth import Login
from infrastructure.api.dto.dto_smtp import EmailRequest
from models import User
from domain.ecommerce.use_case.smtp import send_email_logic
from settings import pwd_context, SECRET_KEY, ALGORITHM
from typing import Optional


http_bearer = HTTPBearer()


async def get_current_user_logic(
    request: Request,
    token: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
):
    print("token", token)
    if token:
        param = token.credentials
        print("param", param)
    try:
        payload = jwt.decode(
            param, SECRET_KEY, algorithms=[ALGORITHM] if ALGORITHM else None
        )
        print("payload", payload)
        sub: str = payload.get("sub")
        if sub is None:
            raise HTTPException(status_code=401, detail="Invalid token: no sub claim")
        user = await User.objects().where(User.id == sub).first()
        if user is None:
            print("No user found with this id")
            raise HTTPException(
                status_code=401,
                detail="Invalid token: no user found with this id",
            )
        return user
    except jwt.PyJWTError as e:
        print("Unable to decode token", str(e))
        raise HTTPException(status_code=401, detail="Invalid token: unable to decode")


async def get_current_active_dealer_logic(
    current_user: User = Depends(get_current_user_logic),
) -> User:
    print(current_user)
    if current_user is not None and current_user.role == "saler":
        return current_user
    raise HTTPException(status_code=400, detail="User is not a saler")


async def get_current_active_buyer_logic(
    current_user: User = Depends(get_current_user_logic),
):
    print(current_user)
    if current_user is not None and current_user.role == "buyer":
        return current_user
    raise HTTPException(status_code=400, detail="User is not a buyer")


async def login_logic(login_data: Login) -> JSONResponse:
    user = (
        await User.objects().where(User.username == login_data.username).first().run()
    )
    if not user or not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    expiration = datetime.utcnow() + timedelta(hours=24)
    payload = {
        "sub": user.id,
        "username": user.username,
        "email": user.email,
        "exp": expiration,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    content = {"access_token": encoded_jwt, "token_type": "bearer", "sub": user.id}
    return JSONResponse(content=content)


async def forgot_password_logic(email: str):
    user = await User.objects().where(User.email == email).first().run()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    reset_link = (
        f"http://localhost:8000/docs#/auth/reset_password_reset_password_post/{user.id}"
    )
    email_request = EmailRequest(
        receiver_email=user.email,
        subject="Reset your password",
        body=f"Click on the following link to reset your password: {reset_link}",
    )
    await send_email_logic(email_request)
    return {"message": "Password reset email sent successfully"}


async def reset_password_logic(user_id: int, new_password: str):
    user = await User.objects().where(User.id == user_id).first().run()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    hashed_password = pwd_context.hash(new_password)
    user.password = hashed_password
    await user.save().run()
    return {"message": "Password reset successfully"}

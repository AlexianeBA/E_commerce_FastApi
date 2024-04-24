from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

import jwt as jwt
from ecommerce.models.auth_models import Login
from ecommerce.tables import User
from ecommerce.settings import pwd_context, SECRET_KEY, ALGORITHM
from typing import Optional

router = APIRouter()
http_bearer = HTTPBearer()


async def get_current_user(
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


async def get_current_active_dealer(
    current_user: User = Depends(get_current_user),
) -> User:
    print(current_user)
    if current_user is not None and current_user.role == "saler":
        return current_user
    raise HTTPException(status_code=400, detail="User is not a saler")


async def get_current_active_buyer(current_user: User = Depends(get_current_user)):
    print(current_user)
    if current_user is not None and current_user.role == "buyer":
        return current_user
    raise HTTPException(status_code=400, detail="User is not a buyer")


@router.post("/login")
async def login(login_data: Login) -> JSONResponse:
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

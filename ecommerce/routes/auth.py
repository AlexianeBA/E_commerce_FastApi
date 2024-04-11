from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, Request, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.security.utils import get_authorization_scheme_param
import jwt as jwt
from models import Login
from tables import User
from settings import pwd_context, SECRET_KEY, ALGORITHM
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


async def get_current_active_dealer(current_user: User = Depends(get_current_user)):
    print(current_user)
    if current_user is not None and current_user.role == "dealer":
        return current_user
    raise HTTPException(status_code=400, detail="User is not a dealer")


@router.post("/login")
async def login(login_data: Login):
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

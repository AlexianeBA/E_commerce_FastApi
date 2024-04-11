from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt as jwt
from fastapi.security.utils import get_authorization_scheme_param
from pydantic import ValidationError
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
    if token:
        scheme, param = get_authorization_scheme_param(token.credentials)
        if scheme.lower() == "bearer":
            try:
                payload = jwt.decode(param, SECRET_KEY, algorithms=[ALGORITHM])
                username: str = payload.get("sub")

                if username is None:
                    print("No sub claim in token")
                    raise HTTPException(
                        status_code=401, detail="Invalid token: no sub claim"
                    )
                return username
            except jwt.PyJWTError:
                print("Unable to decode token")
                raise HTTPException(
                    status_code=401, detail="Invalid token: unable to decode"
                )
    else:
        print("No token provided")
        raise HTTPException(
            status_code=401, detail="Invalid authorization code: no token provided"
        )


async def get_current_active_dealer(current_user: User = Depends(get_current_user)):
    print(current_user)
    if current_user is not None and current_user.role == "dealer":
        return current_user

    raise HTTPException(
        status_code=400,
        detail="L'utilisateur n'est pas  revendeur ou l'utilisateur n'a pas été trouvé",
    )


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
    expiration = datetime.utcnow() + timedelta(minutes=30)
    expiration_timestamp = int(expiration.timestamp())
    payload = {
        "sub": user.id,
        "username": user.username,
        "role": user.role,
        "exp": expiration_timestamp,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    content = {
        "access_token": encoded_jwt,
        "token_type": "bearer",
        "role": user.role,
        "sub": user.id,
        "exp": expiration_timestamp,
    }
    return JSONResponse(content=content)

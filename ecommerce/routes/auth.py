from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse
import jwt as jwt
from models import Login
from tables import User
from settings import pwd_context, SECRET_KEY, ALGORITHM


router = APIRouter()


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
        "username": user.username,
        "email": user.email,
        "exp": expiration,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    content = {"access_token": encoded_jwt, "token_type": "bearer"}
    return JSONResponse(content=content)

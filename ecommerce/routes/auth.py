from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer
import jwt as jwt
from models import Login
from tables import User
from settings import pwd_context, SECRET_KEY, ALGORITHM


router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        algorithms = [ALGORITHM] if ALGORITHM else []
        payload = jwt.decode(token, SECRET_KEY, algorithms=algorithms)
        username: str = payload.get("username")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    user = await User.objects().where(User.username == username).first().run()
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.is_active:
        return current_user
    raise HTTPException(status_code=400, detail="Inactive user")


async def get_current_active_dealer(
    current_user: User = Depends(get_current_active_user),
):
    if current_user.is_dealer == True:
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
        "username": user.username,
        "email": user.email,
        "exp": expiration,
    }
    encoded_jwt = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    content = {"access_token": encoded_jwt, "token_type": "bearer"}
    return JSONResponse(content=content)

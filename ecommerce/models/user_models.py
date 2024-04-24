from typing import Optional
from pydantic import BaseModel
from enum import Enum


class UserType(str, Enum):
    buyer = "buyer"
    saler = "saler"
    admin = "admin"


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    role: UserType


class UserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    role: UserType


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None

    email: Optional[str] = None

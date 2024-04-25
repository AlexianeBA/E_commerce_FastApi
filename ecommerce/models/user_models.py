from typing import Optional
from pydantic import BaseModel
from enum import Enum
from datetime import date


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
    name: str
    email: str
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    role: UserType
    date_of_birth: date
    gender: str
    location: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    name: Optional[str] = None

    email: Optional[str] = None

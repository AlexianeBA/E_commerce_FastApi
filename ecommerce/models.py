from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    stock: int


class ProductIn(BaseModel):
    name: str
    price: int
    stock: int


class UserResponse(BaseModel):
    id: int
    username: str
    password: str
    is_buyer: bool
    is_dealer: bool


class UserRequest(BaseModel):
    username: str
    password: str
    first_name: str
    last_name: str
    email: str
    is_superuser: bool = False
    is_staff: bool = False
    is_active: bool = True
    is_buyer: bool = False
    is_dealer: bool = False
    date_joined: datetime = datetime.now()


class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None


class Login(BaseModel):
    username: str
    password: str

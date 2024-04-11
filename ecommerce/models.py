from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from enum import Enum


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    stock: int


class ProductIn(BaseModel):
    name: str
    price: int
    stock: int


class UserType(str, Enum):
    buyer = "buyer"
    dealer = "dealer"
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


class CartItem(BaseModel):
    product_id: int
    quantity: int


class Cart(BaseModel):
    id: int
    buyer_id: int
    items: list[CartItem]
    total: int
    created_at: datetime


class TokenData(BaseModel):
    username: str
    is_dealer: bool
    is_buyer: bool

from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel
from enum import Enum


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    stock: int
    description: str


class ProductIn(BaseModel):
    name: str
    price: int
    stock: int
    category: str
    rating: int
    on_sale: bool
    is_new: bool
    in_stock: bool
    description: str
    image_url: str
    discount: Optional[int] = None
    discount_end_date: Optional[datetime] = None


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


class OrderItemModel(BaseModel):
    product_id: int
    quantity: int


class OrderModel(BaseModel):
    id: int
    buyer_id: int
    items: List[OrderItemModel]


class ReviewModel(BaseModel):
    product_id: int
    rating: int
    comment: str

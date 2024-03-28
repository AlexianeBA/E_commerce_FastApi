"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

from datetime import datetime
import os
from typing import List, Optional
from piccolo.conf.apps import AppConfig, table_finder
from fastapi import FastAPI, HTTPException
from tables import Product, User
from pydantic import BaseModel
from passlib.context import CryptContext

app = FastAPI()

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
APP_CONFIG = AppConfig(
    app_name="ecommerce",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=table_finder(modules=["tables"], exclude_imported=True),
    migration_dependencies=[],
    commands=[],
)


class ProductModel(BaseModel):
    id: int
    name: str
    price: int
    stock: int


@app.get("/products", response_model=List[ProductModel])
async def get_products():
    products = await Product.select().run()
    return [
        {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
        }
        for product in products
    ]


class ProductIn(BaseModel):
    name: str
    price: int
    stock: int


@app.post("/products/", response_model=ProductModel)
async def create_product(product_data: ProductIn):
    product = Product(
        name=product_data.name, price=product_data.price, stock=product_data.stock
    )
    await product.save().run()
    return product


@app.put("/products/{product_id}", response_model=ProductModel)
async def update_product(product_id: int, product_data: ProductIn):
    product = await Product.objects().where(Product.id == product_id).first().run()
    product.name = product_data.name
    product.price = product_data.price
    product.stock = product_data.stock
    await product.save().run()
    return product


@app.delete("/products/{product_id}")
async def delete_product(product_id: int):
    product = await Product.objects().where(Product.id == product_id).first().run()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        await product.remove().run()
    return {"message": "Product deleted"}


class UserModel(BaseModel):
    id: int
    username: str
    password: str
    is_buyer: bool
    is_dealer: bool


class UserIn(BaseModel):
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


@app.get("/users", response_model=List[UserModel])
async def get_users():
    users = await User.select().run()
    return [
        {
            "id": user["id"],
            "username": user["username"],
            "password": user["password"],
            "is_buyer": user["is_buyer"],
            "is_dealer": user["is_dealer"],
        }
        for user in users
    ]


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@app.post("/users/", response_model=UserModel)
async def create_user(user_data: UserIn):
    hashed_password = pwd_context.hash(user_data.password)
    user = User(
        username=user_data.username,
        password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        email=user_data.email,
        is_superuser=user_data.is_superuser,
        is_staff=user_data.is_staff,
        is_active=user_data.is_active,
        is_buyer=user_data.is_buyer,
        is_dealer=user_data.is_dealer,
        date_joined=user_data.date_joined,
    )
    await user.save().run()
    return UserModel(**user.to_dict())


@app.put("/users/{user_id}", response_model=UserModel)
async def update_user(user_id: int, user_data: UserUpdate):
    user = await User.objects().where(User.id == user_id).first().run()
    if user_data.username is not None:
        user.username = user_data.username
    if user_data.password is not None:
        user.password = pwd_context.hash(user_data.password)
    if user_data.first_name is not None:
        user.first_name = user_data.first_name
    if user_data.last_name is not None:
        user.last_name = user_data.last_name
    if user_data.email is not None:
        user.email = user_data.email
    await user.save().run()
    return UserModel(**user.to_dict())


@app.delete("/users/{user_id}")
async def delete_user(user_id: int):
    user = await User.objects().where(User.id == user_id).first().run()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        await user.remove().run()
    return {"message": "User deleted"}

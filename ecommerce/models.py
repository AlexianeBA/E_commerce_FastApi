import random
from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Boolean,
    Timestamp,
    Serial,
    ForeignKey,
    Date,
)
from datetime import datetime
from enum import Enum
import pandas as pd


class UserType(str, Enum):
    buyer = "buyer"
    saler = "saler"


class Category(str, Enum):
    informatique = "informatique"
    telephonie = "telephonie"
    electromenager = "electromenager"
    mode = "mode"
    beaute = "beaute"
    maison = "maison"
    jardin = "jardin"
    sport = "sport"
    auto = "auto"
    moto = "moto"
    bricolage = "bricolage"
    animalerie = "animalerie"
    jouets = "jouets"
    enfant = "enfant"
    culture = "culture"
    loisirs = "loisirs"
    livres = "livres"
    musique = "musique"
    films = "films"
    instruments = "instruments"
    materiel_professionnel = "materiel_professionnel"
    services = "services"
    autres = "autres"


class Gender(str, Enum):
    female = "female"
    male = "male"


class User(Table, tablename="auth_user"):
    id = Serial(null=False, primary_key=True)
    name = Varchar(length=255, default="")
    username = Varchar(length=255, default="")
    email = Varchar(length=255, default="")
    password = Varchar(length=255, default="")
    is_superuser = Boolean(default=False)
    is_staff = Boolean(default=False)
    is_active = Boolean(default=True)
    role = Varchar(length=255, choices=UserType, default=UserType.buyer.value)
    date_of_birth = Date()
    gender = Varchar(length=255, choices=Gender, default=Gender.male.value)
    location = Varchar(length=255, default="")

    def to_dict(self):
        user_dict = super().to_dict()
        user_dict["date_of_birth"] = self.date_of_birth.isoformat()
        return user_dict


class Product(Table, tablename="dashboard_product"):
    id = Serial(null=False, primary_key=True)
    name = Varchar()
    price = Integer()
    stock = Integer()
    user_id = ForeignKey(User)
    category = Varchar(length=255, choices=Category, default=Category.autres.value)
    rating = Integer()
    in_stock = Boolean(default=True)
    on_sale = Boolean(default=False)
    is_new = Boolean(default=False)
    description = Varchar()
    image_url = Varchar()
    discount = Integer(default=0)
    discount_end_date = Date()
    date_created = Timestamp(default=datetime.now())
    seller_id = ForeignKey(User)

    @property
    async def username(self):
        user = await User.objects().where(User.id == self.user_id).first().run()
        return user.username if user else None


class Review(Table, tablename="review_product"):
    id = Serial(null=False, primary_key=True)
    user_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    rating = Integer()
    comment = Varchar()


class Order(Table, tablename="order_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    total = Integer()
    created_at = Timestamp()


class OrderItem(Table, tablename="order_item"):
    id = Serial(null=False, primary_key=True)
    order_id = ForeignKey(Order)
    product_id = ForeignKey(Product)
    quantity = Integer()
    price = Integer()
    total = Integer()
    created_at = Timestamp()


class Sale(Table, tablename="sale_product"):
    id = Serial(null=False, primary_key=True)
    category = Varchar(length=255, choices=Category, default=Category.autres.value)
    discount = Integer()
    start_date = Date()
    end_date = Date()

    @property
    async def products(self):
        products = (
            await Product.objects().where(Product.category == self.category).run()
        )
        return products


class Purchase(Table, tablename="purchase_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    quantity = Integer()
    total = Integer()
    purchase_date = Timestamp()


class Cart(Table, tablename="cart_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    quantity = Integer()
    total = Integer()
    created_at = Timestamp()
    promotional_code = Varchar()


class PromotionalCode(Table, tablename="promo_code"):
    id = Serial(null=False, primary_key=True)
    code = Varchar()
    discount = Integer()
    start_date = Date()
    end_date = Date()


class OrderStatus(str, Enum):
    pending = "pending"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderPassed(Table, tablename="order_passed"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    status = Varchar(length=255, choices=OrderStatus, default=OrderStatus.pending.value)
    total = ForeignKey(Cart)
    delivery_date = Timestamp()


class SaleProduct(Table, tablename="sale"):
    id = Serial(null=False, primary_key=True)
    order_passed = ForeignKey(OrderPassed)

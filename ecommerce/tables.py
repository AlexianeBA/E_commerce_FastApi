from piccolo.table import Table
from piccolo.columns import Varchar, Integer, Boolean, Timestamp, Serial
from enum import Enum


class Product(Table, tablename="dashboard_product"):
    id = Serial(null=False, primary_key=True)
    name = Varchar()
    price = Integer()
    stock = Integer()


class UserType(str, Enum):
    buyer = "buyer"
    dealer = "dealer"
    admin = "admin"


class User(Table, tablename="auth_user"):
    id = Serial(null=False, primary_key=True)
    first_name = Varchar(length=255, default="")
    last_name = Varchar(length=255, default="")
    username = Varchar(length=255, default="")
    email = Varchar(length=255, default="")
    password = Varchar(length=255, default="")
    is_superuser = Boolean(default=False)
    is_staff = Boolean(default=False)
    is_active = Boolean(default=True)
    role = Varchar(length=255, choices=UserType, default=UserType.buyer.value)
    date_joined = Timestamp()

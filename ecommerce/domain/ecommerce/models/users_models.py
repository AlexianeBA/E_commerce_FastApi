from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Boolean,
    Serial,
    Date,
)

from enum import Enum


class UserType(str, Enum):
    buyer = "buyer"
    saler = "saler"


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

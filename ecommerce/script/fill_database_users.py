import asyncio
import random
import pandas as pd
import secrets


from models import User, UserType
import sys
import bcrypt

from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry

DB = PostgresEngine(
    config={
        "database": "ecommerce_fast_api",
        "user": "postgres",
        "password": "alexiane",
        "host": "localhost",
        "port": 5432,
    }
)
DATABASE_CONFIG = {"default": DB}


async def main():
    df = pd.read_csv("datas/users/users.csv")

    for _, row in df.iterrows():
        password = "password".encode("utf-8")
        hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
        user = User(
            name=row["name"],
            email=row["email"],
            password=hashed_password.decode("utf-8"),
            username=row["username"],
            date_of_birth=random.choice(pd.date_range("1950-01-01", "2000-01-01")),
            gender=row["gender"],
            location=row["location"],
            role=random.choice([UserType.buyer, UserType.saler]),
        )
        await user.save().run()
        print(user)


asyncio.run(main())

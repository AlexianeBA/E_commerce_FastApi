import asyncio
import random
import pandas as pd
import secrets


from tables import User, UserType
import sys

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
    df = pd.read_csv("ecommerce/datas/users/amazon_prime_users.csv")

    for _, row in df.iterrows():
        user = User(
            name=row["Name"],
            email=row["Email Address"],
            password=secrets.token_hex(10),
            username=row["Username"],
            date_of_birth=row["Date of Birth"],
            gender=row["Gender"],
            location=row["Location"],
        )
        await user.save().run()
        print(user)


# Run the main function
asyncio.run(main())

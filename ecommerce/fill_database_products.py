import asyncio
import random
import pandas as pd
from tables import Product, User
from piccolo_conf import DB
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
    df = pd.read_csv("ecommerce/datas/products/Air Conditioners.csv")
    print(df.columns)

    user_ids = User.select(User.id).run_sync()

    for _, row in df.iterrows():
        price = float(row["actual_price"].replace("₹", "").replace(",", ""))
        discount = float(row["discount_price"].replace("₹", "").replace(",", ""))
        rating = float(row["ratings"]) if pd.notnull(row["ratings"]) else None
        user = random.choice(user_ids)
        user_id = user["id"] if isinstance(user, dict) and "id" in user else None
        stock = random.randint(1, 100)
        in_stock = False if stock == 0 else True
        product = Product(
            name=row["name"],
            category=row["sub_category"],
            description="Lorem ipsum dolor sit amet consectetur adipisicing elit.",
            image_url=row["image"],
            rating=rating,
            discount=discount,
            price=price,
            user_id=user_id,
            stock=stock,
            in_stock=in_stock,
        )
        await product.save().run()
        print(product)


asyncio.run(main())

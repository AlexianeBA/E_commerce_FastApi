import asyncio
from models import Order, Product, User


async def clear_tables():
    await Order.alter().drop_table(cascade=True).run()


asyncio.run(clear_tables())

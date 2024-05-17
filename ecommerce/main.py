import asyncio
from fastapi import FastAPI
import uvicorn
from routes import (
    users,
    products,
    auth,
    cart,
    reviews,
    sale,
    purchase,
    promo_code,
    smtp,
    sales_summurary,
    order,
)

from routes.cart import check_orders, check_carts

app = FastAPI()


app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(auth.router, tags=["auth"])
app.include_router(cart.router, tags=["cart"])
app.include_router(reviews.router, tags=["reviews"])
app.include_router(sale.router, tags=["sale"])
app.include_router(purchase.router, tags=["purchase"])
app.include_router(promo_code.router, tags=["promo_code"])
app.include_router(smtp.router, tags=["smtp"])
app.include_router(sales_summurary.router, tags=["sales_summurary"])


uvicorn.run(app, host="localhost", port=8000)

app.on_event("startup")


async def startup_event():
    app.state.check_orders_task = asyncio.create_task(check_orders())
    app.state.check_carts_task = asyncio.create_task(check_carts())


@app.on_event("shutdown")
async def shutdown_event():
    app.state.check_orders_task.cancel()
    app.state.check_carts_task.cancel()
    await app.state.check_carts_task
    await app.state.check_orders_task

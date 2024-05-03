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
)


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

uvicorn.run(app, host="localhost", port=8000)

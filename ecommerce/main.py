from fastapi import FastAPI
from routes import users, products, auth, cart, reviews, sale, purchase, promo_code


app = FastAPI()


app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(auth.router, tags=["auth"])
app.include_router(cart.router, tags=["cart"])
app.include_router(reviews.router, tags=["reviews"])
app.include_router(sale.router, tags=["sale"])
app.include_router(purchase.router, tags=["purchase"])
app.include_router(promo_code.router, tags=["promo_code"])

from fastapi import FastAPI
from routes import users, products, auth, cart


app = FastAPI()


app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(auth.router, tags=["auth"])
app.include_router(cart.router, tags=["cart"])

from fastapi import FastAPI
from routes import users, products, auth

app = FastAPI()

for router in users, products, auth:
    app.include_router(router.router)

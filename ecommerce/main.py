from fastapi import FastAPI
from routes import users, products, auth, cart
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
import time


class TimingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers["Process-Time"] = str(process_time)
        return response


app = FastAPI()

app.add_middleware(TimingMiddleware)

app.include_router(users.router, tags=["users"])
app.include_router(products.router, tags=["products"])
app.include_router(auth.router, tags=["auth"])
app.include_router(cart.router, tags=["cart"])

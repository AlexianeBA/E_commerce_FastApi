from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from routes.auth import get_current_user
from models import SaleProduct, OrderPassed

router = APIRouter()


async def get_current_active_admin(current_user=Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not enough permissions",
        )
    return current_user


@router.get("/orders", dependencies=[Depends(get_current_active_admin)])
async def get_all_orders():
    orders = await OrderPassed.select().run()
    return {"orders": [dict(order) for order in orders]}


@router.get("/orders/delivering", dependencies=[Depends(get_current_active_admin)])
async def get_delivering_orders():
    delivering_orders = (
        await OrderPassed.select().where(OrderPassed.status == "delivering").run()
    )
    return delivering_orders


@router.get("/orders/delivered", dependencies=[Depends(get_current_active_admin)])
async def get_delivered_orders():
    delivered_orders = (
        await OrderPassed.select().where(OrderPassed.status == "delivered").run()
    )
    return delivered_orders


@router.get("/orders/{order_id}", dependencies=[Depends(get_current_active_admin)])
async def get_order(order_id: int):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    return order

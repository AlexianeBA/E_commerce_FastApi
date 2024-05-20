from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from domain.ecommerce.exceptions.exceptions import (
    OrderNotFoundException,
    UnauthorizedException,
)
from domain.ecommerce.use_case.auth import get_current_user_logic
from models.order_models import OrderPassed


async def get_current_active_admin_logic(current_user=Depends(get_current_user_logic)):
    if current_user.role != "admin":
        raise UnauthorizedException(
            "Not enough permissions",
        )
    return current_user


async def get_all_orders_logic():
    orders = await OrderPassed.select().run()
    if not orders:
        raise OrderNotFoundException(
            "No orders found",
        )
    return {"orders": [dict(order) for order in orders]}


async def get_delivering_orders_logic():
    delivering_orders = (
        await OrderPassed.select().where(OrderPassed.status == "delivering").run()
    )
    if not delivering_orders:
        raise OrderNotFoundException(
            "No delivering orders found",
        )
    return delivering_orders


async def get_delivered_orders_logic():
    delivered_orders = (
        await OrderPassed.select().where(OrderPassed.status == "delivered").run()
    )
    if not delivered_orders:
        raise OrderNotFoundException(
            "No delivered orders found",
        )
    return delivered_orders


async def get_order_logic(order_id: int):
    order = await OrderPassed.objects().where(OrderPassed.id == order_id).first().run()
    if not order:
        raise OrderNotFoundException(
            "Order not found",
        )
    return order

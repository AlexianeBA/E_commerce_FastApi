from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from domain.ecommerce.use_case.auth import get_current_user_logic
from domain.ecommerce.use_case.sales_summurary import (
    get_current_active_admin_logic,
    get_all_orders_logic,
    get_delivering_orders_logic,
    get_delivered_orders_logic,
    get_order_logic,
)

router = APIRouter()


@router.get("/orders", dependencies=[Depends(get_current_active_admin_logic)])
async def get_all_orders():
    return await get_all_orders_logic()


@router.get(
    "/orders/delivering", dependencies=[Depends(get_current_active_admin_logic)]
)
async def get_delivering_orders():
    return await get_delivering_orders_logic()


@router.get("/orders/delivered", dependencies=[Depends(get_current_active_admin_logic)])
async def get_delivered_orders():
    return await get_delivered_orders_logic()


@router.get(
    "/orders/{order_id}", dependencies=[Depends(get_current_active_admin_logic)]
)
async def get_order(order_id: int):
    return await get_order_logic(order_id)

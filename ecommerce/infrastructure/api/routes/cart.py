import asyncio
from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from infrastructure.api.dto.dto_cart import (
    CartRequest,
    CartResponse,
    CartItemResponse,
    RefundRequest,
)
from infrastructure.api.dto.dto_payment import PaymentRequest, PaymentResponse
from infrastructure.api.dto.dto_smtp import EmailRequest
from domain.ecommerce.use_case.auth import (
    get_current_active_buyer_logic,
    get_current_user_logic,
)
from domain.ecommerce.exceptions.exceptions import (
    ProductNotFoundException,
    UserNotFoundException,
    ServerError,
)
from domain.ecommerce.models.users_models import User
from domain.ecommerce.models.product_models import Product
from domain.ecommerce.models.cart_models import Cart
from domain.ecommerce.models.order_models import (
    OrderPassed,
    OrderStatus,
    Order,
    OrderItem,
)


from domain.ecommerce.use_case.cart import (
    add_to_cart_logic,
    get_cart_logic,
    get_past_orders_logic,
    checkout_logic,
    cancel_order_logic,
    refund_order_logic,
    remove_from_cart_logic,
    clear_cart_logic,
)

router = APIRouter()


@router.post("/cart", dependencies=[Depends(get_current_active_buyer_logic)])
async def add_to_cart(
    item: CartRequest, current_user=Depends(get_current_user_logic)
) -> JSONResponse:
    try:
        cart: CartResponse = await add_to_cart_logic(item, current_user)
        return JSONResponse(
            content=jsonable_encoder(cart),
            status_code=200,
        )
    except (ProductNotFoundException, UserNotFoundException) as e:
        return JSONResponse(status_code=400, content={"message": str(e)})
    except ServerError as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/cart", dependencies=[Depends(get_current_active_buyer_logic)])
async def get_cart(current_user=Depends(get_current_user_logic)):
    return await get_cart_logic(current_user)  # type: ignore


@router.get("/past_orders", dependencies=[Depends(get_current_active_buyer_logic)])
async def get_past_orders(current_user=Depends(get_current_user_logic)) -> JSONResponse:
    orders = await get_past_orders_logic(current_user)
    return JSONResponse(
        content=jsonable_encoder([order.to_dict() for order in orders]),
        status_code=200,
    )


@router.post("/checkout", dependencies=[Depends(get_current_active_buyer_logic)])
async def checkout(current_user=Depends(get_current_user_logic)):
    return await checkout_logic(current_user)


@router.post(
    "/orders/{order_id}/cancel", dependencies=[Depends(get_current_active_buyer_logic)]
)
async def cancel_order(order_id: int, current_user=Depends(get_current_user_logic)):
    return await cancel_order_logic(order_id, current_user)


@router.post(
    "/orders/{order_id}/refund", dependencies=[Depends(get_current_active_buyer_logic)]
)
async def refund_order(
    order_id: int,
    refund_request: RefundRequest,
    current_user=Depends(get_current_user_logic),
):
    return await refund_order_logic(order_id, refund_request, current_user)


@router.delete(
    "/cart/{item_index}", dependencies=[Depends(get_current_active_buyer_logic)]
)
async def remove_from_cart(
    item_index: int, current_user=Depends(get_current_user_logic)
) -> CartResponse:
    return await remove_from_cart_logic(item_index, current_user)


@router.delete("/cart", dependencies=[Depends(get_current_active_buyer_logic)])
async def clear_cart(current_user=Depends(get_current_user_logic)):
    return await clear_cart_logic(current_user)


async def check_carts():
    while True:
        carts = await Cart.objects().run()
        for cart in carts:
            if datetime.now() - cart.created_at > timedelta(hours=3):
                await cart.delete(force=True).run()
        await asyncio.sleep(3600)


async def check_orders():
    while True:
        orders = await OrderPassed.objects().run()
        for order in orders:
            if (
                order.status == OrderStatus.delivering
                and datetime.now() > order.delivery_date
            ):
                order.status = OrderStatus.delivered
                await order.save().run()
        await asyncio.sleep(3600)

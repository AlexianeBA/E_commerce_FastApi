from datetime import datetime, timedelta
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dto.dto_cart import CartRequest, CartResponse, CartItemResponse
from dto.dto_payment import PaymentRequest, PaymentResponse
from routes.auth import get_current_active_buyer, get_current_user
from models import Product, Order, OrderItem, User, Cart, OrderPassed, OrderStatus

from typing import List

router = APIRouter()

carts = {}


@router.post("/cart", dependencies=[Depends(get_current_active_buyer)])
async def add_to_cart(
    item: CartRequest, current_user=Depends(get_current_user)
) -> CartResponse:
    buyer_id = current_user.id
    user = await User.objects().where(User.id == buyer_id).first().run()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    product = await Product.objects().where(Product.id == item.product_id).first().run()
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    if product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")

    product.stock -= item.quantity
    await product.save().run()

    cart = Cart(
        buyer_id=buyer_id,
        product_id=item.product_id,
        quantity=item.quantity,
        total=int(product.price) * item.quantity,
        created_at=datetime.now(),
    )

    await cart.save().run()

    return CartResponse(
        id=cart.id,
        buyer_id=cart.buyer_id,
        items=[item],
        total=cart.total,
        created_at=cart.created_at,
        promotional_code=cart.promotional_code,
    )


@router.get(
    "/cart",
    dependencies=[Depends(get_current_active_buyer)],
)
async def get_cart(current_user=Depends(get_current_user)):
    user_id = current_user.id
    cart = await Cart.objects().where(Cart.buyer_id == user_id).first().run()
    if cart is None:
        raise HTTPException(status_code=404, detail="Cart not found")
    items = await Cart.objects().where(Cart.buyer_id == user_id).run()
    items_response = [
        CartItemResponse(
            product_id=item.product_id if item.product_id is not None else 0,
            quantity=item.quantity,
            promotional_code=cart.promotional_code,
        ).dict()
        for item in items
    ]
    return {
        "id": cart.id,
        "buyer_id": cart.buyer_id,
        "items": items_response,
        "total": cart.total,
        "created_at": cart.created_at,
        "promotional_code": cart.promotional_code,
    }


@router.delete("/cart/{item_index}", dependencies=[Depends(get_current_active_buyer)])
async def remove_from_cart(
    item_index: int, current_user=Depends(get_current_user)
) -> CartResponse:
    user_id = current_user.id
    if user_id not in carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    if item_index >= len(carts[user_id].items) or item_index < 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart"
        )
    del carts[user_id].items[item_index]
    return carts[user_id]


@router.get(
    "/past_orders",
    dependencies=[Depends(get_current_active_buyer)],
)
async def get_past_orders(current_user=Depends(get_current_user)) -> JSONResponse:
    user_id = current_user.id
    orders = await Order.objects().where(Order.buyer_id == user_id).run()
    if not orders:
        raise HTTPException(
            status_code=400,
            detail="Aucune commande trouvée",
        )
    return JSONResponse(
        content=jsonable_encoder([order.to_dict() for order in orders]),
        status_code=200,
    )


@router.delete("/cart", dependencies=[Depends(get_current_active_buyer)])
async def clear_cart(current_user=Depends(get_current_user)):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()
    for cart_item in cart_items:
        await cart_item.delete(force=True).run()

    return {"message": "Cart cleared successfully"}


@router.post("/checkout", dependencies=[Depends(get_current_active_buyer)])
async def checkout(current_user=Depends(get_current_user)):
    user_id = current_user.id
    cart_items = await Cart.objects().where(Cart.buyer_id == user_id).run()

    if not cart_items:
        raise HTTPException(status_code=400, detail="Cart is empty")

    for cart_item in cart_items:
        await cart_item.delete(force=True).run()
    order = OrderPassed(
        buyer_id=user_id,
        status=OrderStatus.pending,
        delivery_date=datetime.now() + timedelta(days=3),
    )
    await order.save().run()
    return {"message": "Checkout successful, cart cleared"}

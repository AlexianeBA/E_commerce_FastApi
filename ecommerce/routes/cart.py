from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from ecommerce.models.cart_models import CartItem, Cart
from ecommerce.routes.auth import get_current_active_buyer, get_current_user
from ecommerce.tables import Product, Order, OrderItem
from typing import List

router = APIRouter()

carts = {}


@router.post("/cart", dependencies=[Depends(get_current_active_buyer)])
async def add_to_cart(item: CartItem, current_user=Depends(get_current_user)) -> Cart:
    user_id = current_user.id
    product = await Product.objects().where(Product.id == item.product_id).first().run()
    if product is not None and product.stock < item.quantity:
        raise HTTPException(status_code=400, detail="Stock insuffisant")
    if product is not None:
        product.stock -= item.quantity
        await product.save().run()
    if user_id not in carts:
        carts[user_id] = Cart(
            id=user_id,
            items=[item],
            buyer_id=user_id,
            total=0,
            created_at=datetime.now(),
        )
    else:
        carts[user_id].items.append(item)
    return carts[user_id]


@router.get(
    "/cart",
    response_model=Cart,
    dependencies=[Depends(get_current_active_buyer)],
)
async def get_cart(current_user=Depends(get_current_user)) -> Cart:
    user_id = current_user.id
    if user_id not in carts:
        carts[user_id] = Cart(
            id=user_id,
            items=[],
            buyer_id=user_id,
            total=0,
            created_at=datetime.now(),
        )
    return carts[user_id]


@router.delete("/cart/{item_index}", dependencies=[Depends(get_current_active_buyer)])
async def remove_from_cart(
    item_index: int, current_user=Depends(get_current_user)
) -> Cart:
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


@router.post("/checkout", dependencies=[Depends(get_current_active_buyer)])
async def checkout(current_user=Depends(get_current_user)) -> dict:
    buyer_id = current_user.id
    if buyer_id not in carts:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    cart = carts[buyer_id]
    total = 0
    for item in cart.items:
        product = (
            await Product.objects().where(Product.id == item.product_id).first().run()
        )
        if product is not None:
            total += product.price * item.quantity

    order = Order(buyer_id=buyer_id, total=total)
    await order.save().run()

    for item in cart.items:
        product = (
            await Product.objects().where(Product.id == item.product_id).first().run()
        )
        if product is not None and product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail="Stock insuffisant pour un ou plusieurs produits",
            )

        order_item = OrderItem(
            order_id=order.id, product_id=item.product_id, quantity=item.quantity
        )
        await order_item.save().run()

    carts[buyer_id].items = []
    return {"message": "Achat effectué avec succès"}


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

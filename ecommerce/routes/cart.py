from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List

from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from dto.dto_cart import CartRequest, CartResponse, CartItemResponse
from routes.auth import get_current_active_buyer, get_current_user
from models import Product, Order, OrderItem, Cart, PromotionalCode, User

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
        product_id=product,
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
            promotional_code=item.promotional_code,
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


async def process_payment(cart: Cart, user: User):
    # Ici, vous devriez implémenter la logique de paiement réelle
    # Après le paiement réussi, vous pouvez créer une nouvelle commande
    order_items = []
    total_amount = 0
    order = Order(buyer_id=user.id, total=total_amount)
    await order.save().run()

    for item in order_items:
        product = (
            await Product.objects().where(Product.id == item.product_id).first().run()
        )
        if product is None:
            raise HTTPException(status_code=404, detail="Product not found")

        total_amount += product.price * item.quantity
        order_item = OrderItem(
            product_id=product,
            quantity=item.quantity,
            total=product.price * item.quantity,
        )
        order_items.append(order_item)

    order = Order(
        buyer_id=user,
        items=order_items,
        total=total_amount,
        created_at=datetime.now(),
    )
    await order.save().run()
    # Supprimer le panier après avoir passé la commande
    await cart.delete(force=True).run()
    return order


# Endpoint pour effectuer le paiement (checkout)
@router.post("/checkout", dependencies=[Depends(get_current_active_buyer)])
async def checkout(current_user=Depends(get_current_user)):
    user_id = current_user.id
    cart = await Cart.objects().where(Cart.buyer_id == user_id).first().run()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")

    user = await User.objects().where(User.id == user_id).first().run()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    order = await process_payment(cart, user)
    return {
        "message": "Payment processed successfully",
        "order_id": order.id,
    }

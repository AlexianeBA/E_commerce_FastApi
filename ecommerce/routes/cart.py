from datetime import datetime
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models import CartItem, Cart, Order
from routes.auth import get_current_active_buyer, get_current_user
from tables import Product

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
    user_id = current_user.id
    if user_id not in carts:
        raise HTTPException(status_code=404, detail="Panier non trouvé")

    cart = carts[user_id]
    for item in cart.items:
        product = (
            await Product.objects().where(Product.id == item.product_id).first().run()
        )
        if product is not None and product.stock < item.quantity:
            raise HTTPException(
                status_code=400,
                detail="Stock insuffisant pour un ou plusieurs produits",
            )

    for item in cart.items:
        product = (
            await Product.objects().where(Product.id == item.product_id).first().run()
        )
        if product is not None:
            product.stock -= item.quantity
            await product.save().run()

    carts[user_id].items = []
    return {"message": "Achat effectué avec succès"}


from typing import List


@router.get(
    "/past_orders",
    response_model=List[Order],
    dependencies=[Depends(get_current_active_buyer)],
)
async def get_past_orders(current_user=Depends(get_current_user)) -> List[Order]:
    user_id = current_user.id
    if user_id not in Order:
        raise HTTPException(
            status_code=400,
            detail="Aucune commande trouvée",
        )
    return Order.buyer_id == user_id

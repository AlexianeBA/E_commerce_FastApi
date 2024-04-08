from datetime import datetime
from fastapi import APIRouter, HTTPException, status
from typing import List
from models import CartItem, Cart

router = APIRouter()

carts = {}


@router.post("/cart/{user_id}")
async def add_to_cart(user_id: int, item: CartItem):
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


@router.get("/cart/{user_id}", response_model=Cart)
async def get_cart(user_id: int):
    if user_id not in carts:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )
    return carts[user_id]


@router.delete("/cart/{user_id}/{item_index}")
async def remove_from_cart(user_id: int, item_index: int):
    if user_id not in carts or item_index >= len(carts[user_id].items):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found in cart"
        )
    del carts[user_id].items[item_index]
    return carts[user_id]

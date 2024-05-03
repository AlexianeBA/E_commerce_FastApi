from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from dto.dto_purchase import PurchaseModel
from dto.dto_product import ProductRequest
from dto.dto_user import UserRequest
from models import User, Product, Purchase

from typing import List

router = APIRouter()


@router.get("/seller/{seller_id}/buyers")
async def get_buyers_info(seller_id: int) -> JSONResponse:
    products = await Product.select().where(Product.seller_id == seller_id).run()

    if not products:
        raise HTTPException(
            status_code=404, detail="aucun produit trouvé pour ce vendeur"
        )

    product_ids = [product.id for product in products]
    purchases = (
        await Purchase.select().where(Purchase.product_id.is_in(product_ids)).run()
    )

    buyer_ids = set(purchase.user_ for purchase in purchases)
    buyers = await User.select().where(User.id.is_in(list(buyer_ids))).run()

    buyer_info = []
    for buyer in buyers:
        date_of_birth = User.date_of_birth
        age = (datetime.now() - date_of_birth).days // 365
        gender = User.gender
        location = User.location
        buyer_info.append(
            {
                "gender": gender,
                "age": age,
                "location": location,
            }
        )

    return JSONResponse(content=buyer_info)

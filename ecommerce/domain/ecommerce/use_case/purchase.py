from datetime import datetime
from fastapi import HTTPException
from fastapi.responses import JSONResponse
from models.users_models import User
from models.product_models import Product
from models.purchase_models import Purchase


async def get_buyers_info_logic(seller_id: int) -> JSONResponse:
    buyer = await User.select().where(User.id == seller_id).run()
    products = await Product.select().where(Product.seller_id == seller_id).run()

    if not products:
        raise HTTPException(
            status_code=404, detail="aucun produit trouvé pour ce vendeur"
        )

    product_ids = [product.id for product in products]
    purchases = (
        await Purchase.select().where(Purchase.product_id.is_in(product_ids)).run()
    )

    buyer_ids = set(purchase.user_id for purchase in purchases)
    buyers = await User.select().where(User.id.is_in(list(buyer_ids))).run()

    buyer_info = []
    for buyer in buyers:
        date_of_birth = buyer.date_of_birth
        age = (datetime.now() - date_of_birth).days // 365
        gender = buyer.gender
        location = buyer.location
        buyer_info.append(
            {
                "gender": gender,
                "age": age,
                "location": location,
            }
        )

    return JSONResponse(content=buyer_info)

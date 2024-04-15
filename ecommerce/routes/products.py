from typing import List

from fastapi import APIRouter, HTTPException, Depends
from models import ProductIn, ProductModel
from tables import Product
from fastapi.responses import JSONResponse
from routes.auth import get_current_active_dealer, get_current_user
from tables import User

router = APIRouter()


@router.get("/products_of_dealer/{dealer_id}", response_model=List[ProductModel])
async def get_products(current_user: User = Depends(get_current_user)) -> JSONResponse:
    products = await Product.objects().where(Product.user_id == current_user.id).run()
    if products:
        return JSONResponse(
            content=[
                {
                    "id": product["id"],
                    "name": product["name"],
                    "price": float(product["price"]),
                    "stock": product["stock"],
                }
                for product in products
            ]
        )
    else:
        return JSONResponse(
            content={"message": "Aucun produit trouvé"}, status_code=404
        )


@router.get("/products/{product_id}", dependencies=[Depends(get_current_active_dealer)])
async def get_product_details(
    product_id: int, current_user: User = Depends(get_current_user)
) -> JSONResponse:
    product = (
        await Product.objects()
        .where((Product.id == product_id) & (Product.user_id == current_user.id))
        .first()
        .run()
    )

    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    return JSONResponse(
        {
            "id": product.id,
            "name": product.name,
            "price": float(product.price),
            "stock": product.stock,
        }
    )


@router.post(
    "/products/",
    response_model=ProductModel,
    dependencies=[Depends(get_current_active_dealer)],
)
async def create_product(
    product_data: ProductIn, current_user=Depends(get_current_active_dealer)
) -> JSONResponse:
    product = Product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        user_id=current_user.id,
    )
    await product.save().run()
    return JSONResponse(
        content={
            "id": product.id,  # type: ignore
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "message": "Produit créé avec succès",
            "id du vendeur": f"{current_user.id}",
        },
        status_code=201,
    )


@router.put(
    "/products/{product_id}",
    response_model=ProductModel,
    dependencies=[Depends(get_current_active_dealer)],
)
async def update_product(
    product_id: int, product_data: ProductIn, current_user=Depends(get_current_user)
) -> JSONResponse:
    products = (
        await Product.objects()
        .where((Product.id == product_id) & (Product.user_id == current_user.id))
        .run()
    )

    if products:
        product = products[0]
        product.name = product_data.name
        product.price = product_data.price
        product.stock = product_data.stock
        await product.save().run()
        return JSONResponse(
            content={
                "id": product.id,
                "name": product.name,
                "price": product.price,
                "stock": product.stock,
                "message": "Produit mis à jour avec succès",
            },
            status_code=201,
        )
    else:
        raise HTTPException(status_code=404, detail="Produit non trouvé")


@router.delete(
    "/products/{product_id}", dependencies=[Depends(get_current_active_dealer)]
)
async def delete_product(
    product_id: int, current_user=Depends(get_current_user)
) -> JSONResponse:
    product = (
        await Product.objects()
        .where((Product.id == product_id) & (Product.user_id == current_user.id))
        .first()
        .run()
    )
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    else:
        await product.remove().run()
    return JSONResponse({"message": "Produit supprimé avec succès"})

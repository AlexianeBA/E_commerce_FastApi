from typing import List

from fastapi import APIRouter, HTTPException
from models import ProductIn, ProductModel
from tables import Product
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/products", response_model=List[ProductModel])
async def get_products():
    products = await Product.select().run()
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


@router.get("/products/{product_id}")
async def get_product_details(product_id: int):
    product = await Product.objects().where(Product.id == product_id).first().run()
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


@router.post("/products/", response_model=ProductModel)
async def create_product(product_data: ProductIn):
    product = Product(
        name=product_data.name, price=product_data.price, stock=product_data.stock
    )
    await product.save().run()
    return JSONResponse(
        content={
            "id": product.id,  # type: ignore
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "message": "Produit créé avec succès",
        },
        status_code=201,
    )


@router.put("/products/{product_id}", response_model=ProductModel)
async def update_product(product_id: int, product_data: ProductIn):
    product = await Product.objects().where(Product.id == product_id).first().run()
    if product:
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


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    product = await Product.objects().where(Product.id == product_id).first().run()
    if not product:
        raise HTTPException(status_code=404, detail="Produit non trouvé")
    else:
        await product.remove().run()
    return JSONResponse({"message": "Produit supprimé avec succès"})

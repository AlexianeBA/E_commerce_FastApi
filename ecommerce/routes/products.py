from typing import List

from fastapi import APIRouter, HTTPException
from models import ProductIn, ProductModel
from tables import Product

router = APIRouter()


@router.get("/products", response_model=List[ProductModel])
async def get_products():
    products = await Product.select().run()
    return [
        {
            "id": product["id"],
            "name": product["name"],
            "price": product["price"],
            "stock": product["stock"],
        }
        for product in products
    ]


@router.post("/products/", response_model=ProductModel)
async def create_product(product_data: ProductIn):
    product = Product(
        name=product_data.name, price=product_data.price, stock=product_data.stock
    )
    await product.save().run()
    return product


@router.put("/products/{product_id}", response_model=ProductModel)
async def update_product(product_id: int, product_data: ProductIn):
    product = await Product.objects().where(Product.id == product_id).first().run()  # type: ignore
    product.name = product_data.name  # type: ignore
    product.price = product_data.price  # type: ignore
    product.stock = product_data.stock  # type: ignore
    await product.save().run()  # type: ignore
    return product


@router.delete("/products/{product_id}")
async def delete_product(product_id: int):
    product = await Product.objects().where(Product.id == product_id).first().run()  # type: ignore
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    else:
        await product.remove().run()
    return {"message": "Product deleted"}

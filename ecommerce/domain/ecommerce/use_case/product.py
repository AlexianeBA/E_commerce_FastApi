from datetime import date
from typing import Optional

from fastapi import Depends
from domain.ecommerce.exceptions.exceptions import ProductNotFoundException
from domain.ecommerce.use_case.auth import (
    get_current_user_logic,
    get_current_active_dealer_logic,
)
from infrastructure.api.dto.dto_product import ProductRequest, ProductResponse
from models.product_models import Product
from models.users_models import User
from models.review_models import Review
from fastapi.responses import JSONResponse


async def search_products_logic(name: str):
    products_query = Product.objects().where(Product.name.ilike(f"%{name}%"))
    products = await products_query.run()
    if not products:
        raise ProductNotFoundException("Aucun produit trouvé")
    return [
        ProductResponse(**product.to_dict(), created_at=product.date_created)
        for product in products
    ]


async def get_products_logic(
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    category: Optional[str] = None,
    in_stock: Optional[bool] = None,
    on_sale: Optional[bool] = None,
    is_new: Optional[bool] = None,
    description: Optional[str] = None,
    image_url: Optional[str] = None,
    discount: Optional[int] = None,
    created_at: Optional[date] = None,
) -> JSONResponse:
    products_query = Product.objects()

    if min_price is not None:
        products_query = products_query.where(Product.price >= min_price)

    if max_price is not None:
        products_query = products_query.where(Product.price <= max_price)

    if category is not None:
        products_query = products_query.where(Product.category == category)

    if in_stock is not None:
        products_query = products_query.where(Product.in_stock == in_stock)

    if on_sale is not None:
        products_query = products_query.where(Product.on_sale == on_sale)

    if is_new is not None:
        products_query = products_query.where(Product.is_new == is_new)

    if description is not None:
        products_query = products_query.where(Product.description == description)

    if image_url is not None:
        products_query = products_query.where(Product.image_url == image_url)

    if discount is not None:
        products_query = products_query.where(Product.discount == discount)

    if created_at is not None:
        products_query = products_query.where(Product.date_created == created_at)

    products = await products_query.run()

    if not products:
        raise ProductNotFoundException("Aucun produit trouvé")

    product_list = []
    for product in products:
        username = await product.username
        product_dict = product.to_dict()
        if product.date_created is not None:
            product_dict["date_created"] = product.date_created.isoformat()
        product_dict["username_saler"] = username
        reviews = await Review.objects().where(Review.product_id == product.id).run()
        product_dict["reviews"] = [review.to_dict() for review in reviews]

        if product.discount_end_date is not None:
            product_dict["discount_end_date"] = product.discount_end_date.isoformat()

        if product.discount > 0 and (
            product.discount_end_date is None
            or product.discount_end_date >= date.today()
        ):
            product_dict["price"] = product.price * (1 - product.discount / 100)

        product_list.append(product_dict)

    return JSONResponse(
        content=product_list,
        status_code=200,
    )


async def get_product_details_logic(
    product_id: int, current_user: User = Depends(get_current_user_logic)
) -> JSONResponse:
    product = (
        await Product.objects()
        .where((Product.id == product_id) & (Product.user_id == current_user.id))
        .first()
        .run()
    )
    if not product:
        raise ProductNotFoundException("Produit non trouvé")
    return JSONResponse(
        {
            "id": product["id"],
            "name": product["name"],
            "price": float(product["price"]),
            "stock": product["stock"],
            "category": product["category"],
            "rating": product["rating"],
            "in_stock": product["in_stock"],
            "on_sale": product["on_sale"],
            "is_new": product["is_new"],
        }
    )


async def create_product_logic(
    product_data: ProductRequest, current_user=Depends(get_current_active_dealer_logic)
) -> JSONResponse:
    product = Product(
        name=product_data.name,
        price=product_data.price,
        stock=product_data.stock,
        category=product_data.category,
        user_id=current_user.id,
        rating=product_data.rating,
        in_stock=product_data.in_stock,
        on_sale=product_data.on_sale,
        is_new=product_data.is_new,
        description=product_data.description,
        image_url=product_data.image_url,
        discount=product_data.discount,
        discount_end_date=product_data.discount_end_date,
    )
    await product.save().run()
    return JSONResponse(
        content={
            "id": product.id,  # type: ignore
            "name": product.name,
            "price": product.price,
            "stock": product.stock,
            "category": product.category,
            "rating": product.rating,
            "in_stock": product.in_stock,
            "on_sale": product.on_sale,
            "is_new": product.is_new,
            "description": product.description,
            "image_url": product.image_url,
            "discount": product.discount,
            "discount_end_date": product.discount_end_date.isoformat(),
            "message": "Produit créé avec succès",
            "nom du vendeur": f"{current_user.username}",
        },
        status_code=201,
    )


async def update_product_logic(
    product_id: int,
    product_data: ProductRequest,
    current_user=Depends(get_current_user_logic),
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
        raise ProductNotFoundException("Produit non trouvé")


async def delete_product_logic(
    product_id: int, current_user=Depends(get_current_user_logic)
) -> JSONResponse:
    product = (
        await Product.objects()
        .where((Product.id == product_id) & (Product.user_id == current_user.id))
        .first()
        .run()
    )
    if not product:
        raise ProductNotFoundException("Produit non trouvé")
    else:
        await product.remove().run()
    return JSONResponse({"message": "Produit supprimé avec succès"})

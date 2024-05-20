from datetime import date
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Depends
from domain.ecommerce.exceptions.exceptions import ProductNotFoundException
from domain.ecommerce.use_case.product import (
    search_products_logic,
    get_all_products_logic,
    get_product_details_logic,
    create_product_logic,
    update_product_logic,
    delete_product_logic,
)
from domain.ecommerce.use_case.auth import (
    get_current_user_logic,
    get_current_active_dealer_logic,
)
from infrastructure.api.dto.dto_product import ProductRequest, ProductResponse
from models.users_models import User
from fastapi.responses import JSONResponse

router = APIRouter()


@router.get("/products/search")
async def search_products(name: str):
    return await search_products_logic(name)


@router.get("/products")
async def get_all_products(
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
    try:
        return await get_all_products_logic(
            min_price,
            max_price,
            category,
            in_stock,
            on_sale,
            is_new,
            description,
            image_url,
            discount,
            created_at,
        )
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/products/{product_id}")
async def get_product_details(
    product_id: int, current_user: User = Depends(get_current_user_logic)
) -> JSONResponse:
    try:
        return await get_product_details_logic(product_id, current_user)  # type: ignore
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/products")
async def create_product(
    product_data: ProductRequest, current_user=Depends(get_current_active_dealer_logic)
) -> JSONResponse:
    return await create_product_logic(product_data, current_user)


@router.put("/products/{product_id}")
async def update_product(
    product_id: int,
    product_data: ProductRequest,
    current_user=Depends(get_current_user_logic),
) -> JSONResponse:
    try:
        return await update_product_logic(product_id, product_data, current_user)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/products/{product_id}")
async def delete_product(
    product_id: int, current_user=Depends(get_current_user_logic)
) -> JSONResponse:
    try:
        return await delete_product_logic(product_id, current_user)
    except ProductNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))

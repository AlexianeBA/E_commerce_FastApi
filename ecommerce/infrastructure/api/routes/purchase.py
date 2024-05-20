from datetime import datetime
from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from infrastructure.api.dto.dto_purchase import PurchaseModel
from infrastructure.api.dto.dto_product import ProductRequest
from infrastructure.api.dto.dto_user import UserRequest
from domain.ecommerce.models.users_models import User
from domain.ecommerce.models.product_models import Product
from domain.ecommerce.models.purchase_models import Purchase

from domain.ecommerce.use_case.purchase import get_buyers_info_logic
from typing import List


router = APIRouter()


@router.get("/seller/{seller_id}/buyers")
async def get_buyers_info(seller_id: int):
    return await get_buyers_info_logic(seller_id)

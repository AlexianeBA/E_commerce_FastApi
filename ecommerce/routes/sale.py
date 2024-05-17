from fastapi import APIRouter, HTTPException
from dto.dto_sale import SaleIn
from models import Sale, Product

router = APIRouter()

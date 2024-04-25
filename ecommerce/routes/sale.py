from fastapi import APIRouter, HTTPException
from models.sale_models import SaleIn
from tables import Sale, Product

router = APIRouter()


@router.post("/sale/")
async def create_sale(sale: SaleIn):

    products = await Product.objects().where(Product.category == sale.category).run()
    if not products:
        raise HTTPException(status_code=404, detail="Category not found")

    new_sale = Sale(
        category=sale.category,
        discount=sale.discount,
        start_date=sale.start_date,
        end_date=sale.end_date,
    )
    await new_sale.save()
    for product in products:
        product.price = int(product.price * (1 - sale.discount / 100))
        await product.save()

    return {
        "message": f"Sale created for category {sale.category} with discount {sale.discount}% from {sale.start_date} to {sale.end_date}"
    }

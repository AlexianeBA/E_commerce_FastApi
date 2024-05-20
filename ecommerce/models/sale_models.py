from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Serial,
    ForeignKey,
    Date,
)


from models.product_models import Product, Category
from models.order_models import OrderPassed


class Sale(Table, tablename="sale_product"):
    id = Serial(null=False, primary_key=True)
    category = Varchar(length=255, choices=Category, default=Category.autres.value)
    discount = Integer()
    start_date = Date()
    end_date = Date()

    @property
    async def products(self):
        products = (
            await Product.objects().where(Product.category == self.category).run()
        )
        return products


class SaleProduct(Table, tablename="sale"):
    id = Serial(null=False, primary_key=True)
    order_passed = ForeignKey(OrderPassed)

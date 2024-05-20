from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Timestamp,
    Serial,
    ForeignKey,
)

from models.users_models import User
from models.product_models import Product


class Cart(Table, tablename="cart_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    quantity = Integer()
    total = Integer()
    created_at = Timestamp()
    promotional_code = Varchar()

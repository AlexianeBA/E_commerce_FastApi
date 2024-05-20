from piccolo.table import Table
from piccolo.columns import (
    Integer,
    Timestamp,
    Serial,
    ForeignKey,
)


from models.users_models import User
from models.product_models import Product


class Purchase(Table, tablename="purchase_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    quantity = Integer()
    total = Integer()
    purchase_date = Timestamp()

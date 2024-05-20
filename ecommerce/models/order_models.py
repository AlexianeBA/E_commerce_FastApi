from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Timestamp,
    Serial,
    ForeignKey,
)

from enum import Enum

from models.users_models import User
from models.product_models import Product
from models.cart_models import Cart


class Order(Table, tablename="order_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    total = Integer()
    created_at = Timestamp()


class OrderItem(Table, tablename="order_item"):
    id = Serial(null=False, primary_key=True)
    order_id = ForeignKey(Order)
    product_id = ForeignKey(Product)
    quantity = Integer()
    price = Integer()
    total = Integer()
    created_at = Timestamp()


class OrderStatus(str, Enum):
    pending = "pending"
    delivering = "delivering"
    delivered = "delivered"
    cancelled = "cancelled"


class OrderPassed(Table, tablename="order_passed"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    status = Varchar(length=255, choices=OrderStatus, default=OrderStatus.pending.value)
    total = ForeignKey(Cart)
    delivery_date = Timestamp()

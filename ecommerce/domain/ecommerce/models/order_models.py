import random
from piccolo.table import Table
from piccolo.columns import (
    Varchar,
    Integer,
    Boolean,
    Timestamp,
    Serial,
    ForeignKey,
    Date,
)
from datetime import datetime
from enum import Enum
import pandas as pd
from domain.ecommerce.models.users_models import User
from domain.ecommerce.models.product_models import Product
from domain.ecommerce.models.cart_models import Cart


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

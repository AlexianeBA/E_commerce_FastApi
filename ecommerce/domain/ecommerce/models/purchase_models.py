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


class Purchase(Table, tablename="purchase_product"):
    id = Serial(null=False, primary_key=True)
    buyer_id = ForeignKey(User)
    product_id = ForeignKey(Product)
    quantity = Integer()
    total = Integer()
    purchase_date = Timestamp()

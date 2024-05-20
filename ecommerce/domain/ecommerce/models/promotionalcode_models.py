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


class PromotionalCode(Table, tablename="promo_code"):
    id = Serial(null=False, primary_key=True)
    code = Varchar()
    discount = Integer()
    start_date = Date()
    end_date = Date()

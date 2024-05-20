from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class Product(Table, tablename="dashboard_product", schema=None):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name=None,
        secret=False,
    )


ID = "2024-05-03T15:43:34:721378"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Cart",
        tablename="cart_product",
        column_name="product_id",
        db_column_name="product_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Product,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Cart",
        tablename="cart_product",
        column_name="quantity",
        db_column_name="quantity",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.alter_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="date_created",
        db_column_name="date_created",
        params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=15, second=34, microsecond=715929
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=15, second=11, microsecond=913573
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    return manager

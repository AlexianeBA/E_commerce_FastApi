from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class OrderPassed(Table, tablename="order_passed", schema=None):
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


ID = "2024-05-17T11:44:55:440249"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="OrderPassed",
        tablename="order_passed",
        column_name="price",
        db_column_name="price",
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
                year=2024, month=5, day=5, hour=11, second=55, microsecond=434216
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=11, second=30, microsecond=29635
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    manager.alter_column(
        table_class_name="SaleProduct",
        tablename="sale",
        column_name="order_passed",
        db_column_name="order_passed",
        params={"references": OrderPassed},
        old_params={"references": Product},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
        schema=None,
    )

    return manager

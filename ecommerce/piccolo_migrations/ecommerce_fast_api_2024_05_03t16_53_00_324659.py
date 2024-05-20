from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Timestamp
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.defaults.timestamp import TimestampNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class User(Table, tablename="auth_user", schema=None):
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


ID = "2024-05-03T16:53:00:324659"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_table(
        class_name="OrderPassed",
        tablename="order_passed",
        schema=None,
        columns=None,
    )

    manager.add_column(
        table_class_name="OrderPassed",
        tablename="order_passed",
        column_name="id",
        db_column_name="id",
        column_class_name="Serial",
        column_class=Serial,
        params={
            "null": False,
            "primary_key": True,
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
        table_class_name="OrderPassed",
        tablename="order_passed",
        column_name="buyer_id",
        db_column_name="buyer_id",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": User,
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
        table_class_name="OrderPassed",
        tablename="order_passed",
        column_name="status",
        db_column_name="status",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "pending",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "OrderStatus",
                {
                    "pending": "pending",
                    "delivering": "delivering",
                    "delivered": "delivered",
                    "cancelled": "cancelled",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="OrderPassed",
        tablename="order_passed",
        column_name="delivery_date",
        db_column_name="delivery_date",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampNow(),
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
                year=2024, month=5, day=5, hour=16, second=0, microsecond=318785
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=15, second=34, microsecond=715929
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    return manager

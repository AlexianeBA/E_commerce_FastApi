from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Serial
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


ID = "2024-04-19T17:30:32:860733"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Order",
        tablename="order_product",
        column_name="buyer_id",
        db_column_name="buyer_id",
        params={"references": User},
        old_params={"references": Product},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
        schema=None,
    )

    return manager

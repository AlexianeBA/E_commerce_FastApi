from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Date
from piccolo.columns.column_types import Integer
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.indexes import IndexMethod


ID = "2024-04-19T14:14:55:741662"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="discount",
        db_column_name="discount",
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

    manager.add_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="discount_end_date",
        db_column_name="discount_end_date",
        column_class_name="Date",
        column_class=Date,
        params={
            "default": DateNow(),
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

    return manager

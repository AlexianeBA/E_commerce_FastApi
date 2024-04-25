from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom
from piccolo.columns.indexes import IndexMethod


ID = "2024-04-25T16:56:02:472339"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="date_created",
        db_column_name="date_created",
        column_class_name="Timestamp",
        column_class=Timestamp,
        params={
            "default": TimestampCustom(
                year=2024, month=4, day=4, hour=16, second=2, microsecond=468703
            ),
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

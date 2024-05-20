from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2024-05-17T11:46:10:362272"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.rename_column(
        table_class_name="OrderPassed",
        tablename="order_passed",
        old_column_name="price",
        new_column_name="total",
        old_db_column_name="price",
        new_db_column_name="total",
        schema=None,
    )

    manager.alter_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="date_created",
        db_column_name="date_created",
        params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=11, second=10, microsecond=355287
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=11, second=55, microsecond=434216
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    return manager

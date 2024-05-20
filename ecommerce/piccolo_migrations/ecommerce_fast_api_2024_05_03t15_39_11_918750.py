from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2024-05-03T15:39:11:918750"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.drop_table(class_name="CartItem", tablename="cart_item", schema=None)

    manager.alter_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="date_created",
        db_column_name="date_created",
        params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=15, second=11, microsecond=913573
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=16, second=6, microsecond=546176
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    return manager

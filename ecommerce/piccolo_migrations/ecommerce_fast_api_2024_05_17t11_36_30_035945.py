from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.column_types import Timestamp
from piccolo.columns.defaults.timestamp import TimestampCustom


ID = "2024-05-17T11:36:30:035945"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="SaleProduct",
        tablename="sale",
        column_name="quantity",
        db_column_name="quantity",
        schema=None,
    )

    manager.drop_column(
        table_class_name="SaleProduct",
        tablename="sale",
        column_name="seller_id",
        db_column_name="seller_id",
        schema=None,
    )

    manager.drop_column(
        table_class_name="SaleProduct",
        tablename="sale",
        column_name="total",
        db_column_name="total",
        schema=None,
    )

    manager.rename_column(
        table_class_name="SaleProduct",
        tablename="sale",
        old_column_name="product_id",
        new_column_name="order_passed",
        old_db_column_name="product_id",
        new_db_column_name="order_passed",
        schema=None,
    )

    manager.alter_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="date_created",
        db_column_name="date_created",
        params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=11, second=30, microsecond=29635
            )
        },
        old_params={
            "default": TimestampCustom(
                year=2024, month=5, day=5, hour=11, second=38, microsecond=202994
            )
        },
        column_class=Timestamp,
        old_column_class=Timestamp,
        schema=None,
    )

    return manager

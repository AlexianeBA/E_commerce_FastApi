from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-04-19T15:34:56:771756"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.drop_table(class_name="Order", tablename="order_product", schema=None)

    return manager

from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-04-19T16:41:49:881382"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.rename_column(
        table_class_name="Product",
        tablename="dashboard_product",
        old_column_name="descritpion",
        new_column_name="description",
        old_db_column_name="descritpion",
        new_db_column_name="description",
        schema=None,
    )

    return manager

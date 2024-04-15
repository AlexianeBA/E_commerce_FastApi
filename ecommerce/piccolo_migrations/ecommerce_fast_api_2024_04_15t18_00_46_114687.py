from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-04-15T18:00:46:114687"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.drop_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="date_joined",
        db_column_name="date_joined",
        schema=None,
    )

    return manager

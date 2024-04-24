from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Date
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.date import DateNow


ID = "2024-04-23T18:51:27:384098"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="date_of_birth",
        db_column_name="date_of_birth",
        params={"default": DateNow()},
        old_params={"default": ""},
        column_class=Date,
        old_column_class=Varchar,
        schema=None,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="gender",
        db_column_name="gender",
        params={
            "default": "male",
            "choices": Enum("Gender", {"female": "female", "male": "male"}),
        },
        old_params={"default": "", "choices": None},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager

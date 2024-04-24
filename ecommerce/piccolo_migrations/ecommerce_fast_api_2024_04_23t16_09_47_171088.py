from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Varchar
from piccolo.columns.indexes import IndexMethod


ID = "2024-04-23T16:09:47:171088"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.add_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="location",
        db_column_name="location",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
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
        table_class_name="User",
        tablename="auth_user",
        column_name="name",
        db_column_name="name",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
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

    manager.rename_column(
        table_class_name="User",
        tablename="auth_user",
        old_column_name="first_name",
        new_column_name="date_of_birth",
        old_db_column_name="first_name",
        new_db_column_name="date_of_birth",
        schema=None,
    )

    manager.rename_column(
        table_class_name="User",
        tablename="auth_user",
        old_column_name="last_name",
        new_column_name="gender",
        old_db_column_name="last_name",
        new_db_column_name="gender",
        schema=None,
    )

    manager.alter_column(
        table_class_name="User",
        tablename="auth_user",
        column_name="role",
        db_column_name="role",
        params={
            "choices": Enum("UserType", {"buyer": "buyer", "saler": "saler"})
        },
        old_params={
            "choices": Enum(
                "UserType", {"buyer": "buyer", "saler": "saler", "admin": "admin"}
            )
        },
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager

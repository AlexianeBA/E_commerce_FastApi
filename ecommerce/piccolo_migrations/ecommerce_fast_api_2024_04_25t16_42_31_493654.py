from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Date
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.date import DateNow
from piccolo.columns.indexes import IndexMethod


ID = "2024-04-25T16:42:31:493654"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.rename_table(
        old_class_name="DashboardSaler",
        old_tablename="dashboard_saler",
        new_class_name="Sale",
        new_tablename="sale_product",
        schema=None,
    )

    manager.drop_column(
        table_class_name="Sale",
        tablename="sale_product",
        column_name="buyer_id",
        db_column_name="buyer_id",
        schema=None,
    )

    manager.add_column(
        table_class_name="Sale",
        tablename="sale_product",
        column_name="category",
        db_column_name="category",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "autres",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Category",
                {
                    "informatique": "informatique",
                    "telephonie": "telephonie",
                    "electromenager": "electromenager",
                    "mode": "mode",
                    "beaute": "beaute",
                    "maison": "maison",
                    "jardin": "jardin",
                    "sport": "sport",
                    "auto": "auto",
                    "moto": "moto",
                    "bricolage": "bricolage",
                    "animalerie": "animalerie",
                    "jouets": "jouets",
                    "enfant": "enfant",
                    "culture": "culture",
                    "loisirs": "loisirs",
                    "livres": "livres",
                    "musique": "musique",
                    "films": "films",
                    "instruments": "instruments",
                    "materiel_professionnel": "materiel_professionnel",
                    "services": "services",
                    "autres": "autres",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Sale",
        tablename="sale_product",
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
        table_class_name="Sale",
        tablename="sale_product",
        column_name="end_date",
        db_column_name="end_date",
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

    manager.add_column(
        table_class_name="Sale",
        tablename="sale_product",
        column_name="start_date",
        db_column_name="start_date",
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

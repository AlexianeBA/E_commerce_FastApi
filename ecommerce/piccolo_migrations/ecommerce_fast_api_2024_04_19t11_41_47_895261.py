from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.column_types import Varchar


ID = "2024-04-19T11:41:47:895261"
VERSION = "1.5.0"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="ecommerce_fast_api", description=DESCRIPTION
    )

    manager.alter_column(
        table_class_name="Product",
        tablename="dashboard_product",
        column_name="category",
        db_column_name="category",
        params={
            "default": "autres",
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
        },
        old_params={"default": "", "choices": None},
        column_class=Varchar,
        old_column_class=Varchar,
        schema=None,
    )

    return manager

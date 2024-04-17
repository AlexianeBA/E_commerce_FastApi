"""
Import all of the Tables subclasses in your app here, and register them with
the APP_CONFIG.
"""

# TODO: revoir les modèles Prodcts
# TODO: FK pour buyer par rapport aux produits
# TODO: mettre en place la paiement (paiement, vérification, validation)
# TODO: ajouter des filtres produits
# TODO: typage
# TODO: tests unitaires


import os

from piccolo.conf.apps import AppConfig, table_finder
import os

CURRENT_DIRECTORY = os.path.dirname(os.path.abspath(__file__))
APP_CONFIG = AppConfig(
    app_name="ecommerce_fast_api",
    migrations_folder_path=os.path.join(CURRENT_DIRECTORY, "piccolo_migrations"),
    table_classes=table_finder(modules=["tables"], exclude_imported=True),
    migration_dependencies=[],
    commands=[],
)

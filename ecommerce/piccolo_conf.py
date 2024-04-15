from piccolo.engine.postgres import PostgresEngine
from piccolo.conf.apps import AppRegistry

DB = PostgresEngine(
    config={
        "database": "ecommerce_fast_api",
        "user": "postgres",
        "password": "alexiane",
        "host": "localhost",
        "port": 5432,
    }
)

APP_REGISTRY = AppRegistry(apps=["piccolo_app"])

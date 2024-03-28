from piccolo.engine.postgres import PostgresEngine

DB = PostgresEngine(
    config={
        "database": "ecommerce",
        "user": "alexiane",
        "password": "alexiane",
        "host": "localhost",
        "port": 5432,
    }
)

import psycopg
from app.core.config import settings
from psycopg import sql

with psycopg.connect(
    settings.PSYCOPG_URL, autocommit=True
) as conn:
    with conn.cursor() as cur:
        cur.execute(sql.SQL("CREATE DATABASE {}")
                    .format(sql.Identifier(
                        settings.DATABASE_NAME
                        )))
        print("Database created successfully.")
    
from functools import lru_cache
import psycopg
from psycopg_pool import AsyncConnectionPool
from app.config import get_settings

settings = get_settings()

conninfo = f"dbname={settings.db_name} host={settings.db_host} user={settings.db_user} password={settings.db_password} port={settings.db_port}"

def get_conn():
    return psycopg.connect(conninfo=conninfo, autocommit=True)

@lru_cache()
def get_async_pool():
    return AsyncConnectionPool(conninfo=conninfo, open=False)
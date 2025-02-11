import asyncio
import asyncpg
from logger import logger
async def get_conn_db():
    conn = None
    try:
        # bad, need load from .env file
        conn = await asyncpg.connect(user='postgres', password='ZaqZaq123', database='test', host='localhost', port=5432)
    except Exception as e:
        logger.error("cheto poshlo ne tak", exc_info=e)
        return None
    finally:
        return conn

async def _create_user(conn: asyncpg.connection.Connection,
                      f_name: str,
                      l_name: str,
                      password: str):
    try:

        bad_query = f"INSERT INTO user_table (first_name, last_name, password) VALUES ('{f_name}', '{l_name}', '{password}')"
        good_query = "INSERT INTO user_table (first_name, last_name, password) VALUES ($1, $2, $3)"
        await conn.execute(bad_query)
        return "vse ok"
    except Exception as e:
        logger.error("cheto poshlo ne tak v zaprose", exc_info=e)
        return None
    # await conn.execute(good_query, f_name, l_name, password) # good execute

async def _good_create_user(conn: asyncpg.connection.Connection,
                      f_name: str,
                      l_name: str,
                      password: str):
    try:

        good_query = "INSERT INTO user_table (first_name, last_name, password) VALUES ($1, $2, $3)"
        await conn.execute(good_query, f_name, l_name, password)
        return "vse ok"
    except Exception as e:
        logger.error("cheto poshlo ne tak v zaprose", exc_info=e)
        return None
    # await conn.execute(good_query, f_name, l_name, password) # good execute

async def _get_users(conn: asyncpg.connection.Connection):
    try:
        pass
    except Exception as e:
        logger.error("cheto poshlo ne tak v zaprose", exc_info=e)
import asyncpg
import logging

from logger import logger

# Подключение к базе данных через сервис db из Docker Compose
async def get_conn_db():
    conn = None
    try:
        conn = await asyncpg.connect(
            user='postgres',
            password='ZaqZaq123',
            database='test',
            host='db',
            port=5432
        )
    except Exception as e:
        logger.error("Ошибка подключения к базе данных", exc_info=e)
        return None
    finally:
        return conn

# Уязвимая функция с SQL-инъекцией (создание пользователя)
async def _create_user(conn: asyncpg.connection.Connection,
                      f_name: str,
                      l_name: str,
                      password: str):
    try:
        bad_query = f"INSERT INTO user_table (first_name, last_name, password) VALUES ('{f_name}', '{l_name}', '{password}')"
        logger.info(bad_query)
        result = await conn.execute(bad_query)
        logger.info(f"result: {result}")
        return result
    except Exception as e:
        logger.error("Ошибка в запросе", exc_info=e)
        return None

# Безопасная функция для создания пользователя
async def _good_create_user(conn: asyncpg.connection.Connection,
                           f_name: str,
                           l_name: str,
                           password: str):
    try:
        good_query = "INSERT INTO user_table (first_name, last_name, password) VALUES ($1, $2, $3)"
        result = await conn.execute(good_query, f_name, l_name, password)
        logger.info(f"result: {result}")
        return "vse ok"
    except Exception as e:
        logger.error("Ошибка в запросе", exc_info=e)
        return None

# Уязвимая функция с SQL-инъекцией (поиск пользователя)
async def find_user(conn: asyncpg.connection.Connection,
                    f_name: str):
    try:
        bad_query = f"SELECT * FROM user_table WHERE first_name = '{f_name}'"
        logger.info(bad_query)
        result = await conn.fetchrow(bad_query)
        logger.info(f"result: {result}")
        return result
    except Exception as e:
        logger.error("Ошибка в запросе", exc_info=e)
        return None
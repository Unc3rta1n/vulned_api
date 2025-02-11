from fastapi import FastAPI
import asyncpg
from logger import logger
from db import get_conn_db, _create_user, _good_create_user

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/bad_create_user")
async def create_user(f_name:str, l_name:str, password:str):
    conn = await get_conn_db()
    logger.info(f"{conn =} {type(conn)}")
    result = await _create_user(conn, f_name, l_name, password)
    if result is None:
        return {"message": "Something went wrong"}
    else:
        return {"message": "User created successfully"}


@app.post("/good_create_user")
async def create_user(f_name:str, l_name:str, password:str):
    conn = await get_conn_db()
    logger.info(f"{conn =} {type(conn)}")
    result = await _good_create_user(conn, f_name, l_name, password)
    if result is None:
        return {"message": "Something went wrong"}
    else:
        return {"message": "User created successfully"}
@app.get("/users")
async def get_users():
    conn = await get_conn_db()
    logger.info(f"{conn =} {type(conn)}")
    user_list = await _get_users(conn)

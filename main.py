from fastapi import FastAPI, HTTPException
import asyncpg
import logging
from db import get_conn_db, _create_user, _good_create_user, find_user
import os
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter  # Добавляем для кастомных метрик

# Настройка логирования

from logger import logger
app = FastAPI()

# Инициализация Prometheus
instrumentator = Instrumentator().instrument(app)
instrumentator.expose(app, endpoint="/metrics")

# Кастомные метрики
DB_ERRORS = Counter('db_errors_total', 'Total number of database errors')
SQL_INJECTION_ATTEMPTS = Counter('sql_injection_attempts_total', 'Total number of SQL injection attempts')
LFI_EXECUTIONS = Counter('lfi_executions_total', 'Total number of LFI executions')

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/bad_create_user")
async def create_user(f_name: str, l_name: str, password: str):
    conn = await get_conn_db()
    logger.info(f"{conn =} {type(conn)}")
    if "'" in f_name or ";" in f_name:  # Простая проверка на инъекцию
        SQL_INJECTION_ATTEMPTS.inc()
    result = await _create_user(conn, f_name, l_name, password)
    if result is None:
        DB_ERRORS.inc()  # Увеличиваем счетчик ошибок базы
        return {"message": "Something went wrong"}
    return {"message": "User created successfully"}

@app.get("/good_create_user")
async def good_create_user(f_name: str, l_name: str, password):
    conn = await get_conn_db()
    logger.info(f"{conn =} {type(conn)}")
    result = await _good_create_user(conn, f_name, l_name, password)
    if result is None:
        DB_ERRORS.inc()
        return {"message": "Something went wrong"}
    return {"message": "User created successfully"}

@app.get("/find_user")
async def get_user(f_name: str):
    logger.info(f"/find_user {f_name}")
    if "'" in f_name or ";" in f_name:  # Простая проверка на инъекцию
        SQL_INJECTION_ATTEMPTS.inc()
    conn = await get_conn_db()
    result = await find_user(conn, f_name)
    if result:
        return {"message": "User found successfully", "user": dict(result)}
    return {"message": "User not found"}

@app.get("/read_file/{filepath:path}")
async def read_file(filepath: str):
    try:
        with open(filepath, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

BASE_DIR = "/app/allowed_files/"
@app.get("/fixed_read_file/{filepath:path}")
async def fixed_read_file(filepath: str):
    full_path = os.path.join(BASE_DIR, filepath)
    if not full_path.startswith(BASE_DIR) or ".." in filepath:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        with open(full_path, "r") as f:
            return {"content": f.read()}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/include_file")
async def include_file(filename: str):
    try:
        file_path = f"/app/{filename}"
        with open(file_path, "r") as f:
            content = f.read()
        exec(content)
        LFI_EXECUTIONS.inc()  # Увеличиваем счетчик при выполнении LFI
        return {"included_file": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/fixed_include_file")
async def fixed_include_file(filename: str):
    base_dir = "/app/allowed_files/"
    file_path = os.path.join(base_dir, filename)
    if not file_path.startswith(base_dir) or ".." in filename:
        raise HTTPException(status_code=403, detail="Access denied")
    try:
        with open(file_path, "r") as f:
            content = f.read()
        return {"included_file": content}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
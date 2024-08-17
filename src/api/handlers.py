import asyncio
import logging
import secrets
import sys

import tarantool
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schemas.data import KeyBatch, KVBatch

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(stream=sys.stdout))

router = APIRouter()

conn = tarantool.Connection(host='tarantool', port=3301)

users_db = {'admin': 'presale'}

tokens_db = {}


# Получение токена
@router.post('/login')
async def auth_user(form_data: OAuth2PasswordRequestForm = Depends()) -> dict:
    username = form_data.username
    if username in users_db:
        if form_data.password==users_db[username]:
            token = secrets.token_urlsafe(10)
            tokens_db[token] = username
            logger.info(f'User logged in: {username}')
            return {'access_token': token}
        else:
            logger.info(f'Failed authorization attempt for user {username}: wrong password')
            raise HTTPException(status_code=400, detail='Wrong password')
    else:
        logger.info(f'Failed authorization attempt for user {username}: username not found')
        raise HTTPException(status_code=400, detail='Username not found')


oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/login')


# Вернуть пользователя по токену
def get_current_user(token: str = Depends(oauth2_scheme)) -> str:
    if token not in tokens_db:
        raise HTTPException(status_code=401, detail="Invalid token")
    return tokens_db[token]


# Запись данных
async def replace_in_tarantool(key, value):
    try:
        conn.space('kv_storege').replace((key, value))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to insert {key}: {str(e)}")


@router.post('/write')
async def write_data(batch: KVBatch, username: str = Depends(get_current_user)) -> dict:
    try:
        tasks = []
        for key, value in batch.data.items():
            tasks.append(replace_in_tarantool(key, value))
        await asyncio.gather(*tasks)

        logger.info(f'User {username} added new entries.')
        return {"status": "success"}
    except Exception as e:
        logger.info(f'Unsuccessful attempt to write data by user {username}')
        raise HTTPException(status_code=500, detail=str(e))


# Чтение данных
async def fetch_from_tarantool(key):
    try:
        result = conn.space('kv_storege').select(key)
        return key, result[0][1] if result else None
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch {key}: {str(e)}")


@router.post('/read')
async def read_data(batch: KeyBatch, username: str = Depends(get_current_user)) -> dict:
    try:
        tasks = []
        for key in batch.keys:
            tasks.append(fetch_from_tarantool(key))

        results = await asyncio.gather(*tasks)

        data = {key: value for key, value in results}

        logger.info(f'User {username} retrieved data for keys: {list(batch.keys)}.')
        return {"data": data}
    except Exception as e:
        logger.info(f'Unsuccessful attempt to read data by user {username}')
        raise HTTPException(status_code=500, detail=str(e))

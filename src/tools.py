import json
import logging
from os import mkdir
from os.path import abspath, dirname, isdir
from time import strftime, localtime, time

import aiohttp
import motor.motor_asyncio
from bson import ObjectId
from retrying import retry

from config import config

ABSPATH = dirname(abspath(__file__))
fake_headers = {
    'Accept-Language': 'en-US,en;q=0.8',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0',
}


@retry(wait_fixed=config['error_sec'])
async def get(url: str) -> str:
    if config['enable_proxy']:
        async with aiohttp.ClientSession(headers=fake_headers) as session:
            async with session.get(url, proxy=f'http://{config["proxy"]}') as resp:
                return await resp.text()
    else:
        async with aiohttp.ClientSession(headers=fake_headers) as session:
            async with session.get(url) as resp:
                return await resp.text()


async def get_json(url: str) -> dict:
    try:
        return json.loads(await get(url))
    except json.decoder.JSONDecodeError:
        logger = logging.getLogger('run.get_json')
        logger.exception('Load Json Error')


def get_logger():
    if not isdir('log'):
        mkdir('log')
    logger = logging.getLogger('run')
    today = strftime('%m-%d', localtime(time()))
    stream_handler = logging.StreamHandler()
    file_handler = logging.FileHandler(filename=f"log/log-{today}.log")
    formatter = logging.Formatter("%(asctime)s[%(levelname)s]: %(filename)s[line:%(lineno)d] - %(name)s : %(message)s")
    stream_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)
    stream_handler.setLevel(logging.DEBUG)
    file_handler.setLevel(logging.WARNING)
    logger.setLevel(logging.DEBUG)
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return logger


class Database:
    def __init__(self, db: str):
        client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://127.0.0.1:27017')
        _db = client["Video"]
        self.db = _db[db]
        self.logger = logging.getLogger('run.db')

    async def select(self):
        cursor = self.db.find({})
        return await cursor.to_list(None)

    async def delete(self, _id):
        result = await self.db.delete_many({'_id': ObjectId(_id)})

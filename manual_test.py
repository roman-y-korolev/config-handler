import asyncio
import logging
import os

from conf import DB_CONFIG, DB_CONFIG_TEST, DB_CONFIG_DEV
from models.config import Configs
from utils.database import get_engine, db


async def main():
    c = Configs(tenant='1', integration_type='2', username='12345')
    await c.create_or_update()
    print(await Configs.get(tenant='1', integration_type='2'))


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.INFO)

loop = asyncio.get_event_loop()

ENV = os.environ['APP_ENV']
if ENV == 'PROD':
    config = DB_CONFIG
elif ENV == 'DEV':
    config = DB_CONFIG_DEV
else:
    config = DB_CONFIG_TEST

db['engine'] = loop.run_until_complete(get_engine(db_config=config))

loop.run_until_complete(main())
loop.close()

import asyncio
import logging
import os
import time

from aiohttp import web
from psycopg2 import OperationalError

from api.config import ConfigEndpoint
from api.login import LoginEndpoint
from api.users import UserEndpoint
from conf import DB_CONFIG, DB_CONFIG_TEST, DB_CONFIG_DEV
from utils.database import get_engine, db, create_all_tables

logger = logging.getLogger(__name__)


def app_factory():
    """
    Application factory
    :return: aiohttp application
    :rtype: aiohttp.web_app.Application
    """
    loop = asyncio.get_event_loop()
    app = web.Application()

    ENV = os.environ['APP_ENV']
    if ENV == 'PROD':
        config = DB_CONFIG
    elif ENV == 'DEV':
        config = DB_CONFIG_DEV
    else:
        config = DB_CONFIG_TEST
    connected = False
    times = 0
    while not connected and times < 5:
        try:
            db['engine'] = loop.run_until_complete(get_engine(db_config=config))
            connected = True
        except OperationalError:
            logger.warning('can not connect to the database')
            time.sleep(5)
            times += 1

    loop.run_until_complete(create_all_tables())

    app.router.add_route('POST', '/user', UserEndpoint.post)
    app.router.add_route('GET', '/login', LoginEndpoint.get)

    app.router.add_route('POST', '/config', ConfigEndpoint.post)
    app.router.add_route('GET', '/config', ConfigEndpoint.get)

    logger.info('Application is created')
    return app

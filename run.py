import logging
import os

from aiohttp import web

from utils import factory

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logging.getLogger().setLevel(logging.DEBUG)

app = factory.app_factory()
PORT = os.environ['APP_PORT']
web.run_app(app, port=PORT)

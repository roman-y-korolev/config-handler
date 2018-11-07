import asyncio
import sys

from utils.database import create_all_tables, drop_all_tables
from utils.factory import app_factory

if __name__ == '__main__':
    app_factory()
    loop = asyncio.get_event_loop()
    if sys.argv[1] == 'create':
        loop.run_until_complete(drop_all_tables())
        loop.run_until_complete(create_all_tables())
    elif sys.argv[1] == 'drop':
        loop.run_until_complete(drop_all_tables())

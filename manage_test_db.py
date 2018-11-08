import asyncio
import sys

from models.config import Configs
from models.users import Users
from utils.database import create_all_tables, drop_all_tables
from utils.factory import app_factory


async def fill_db_with_test_data():
    """
    Fill database with test data
    :return: None
    :rtype: None
    """
    user = Users(login='test_login', password='test_password')
    await user.create()
    config = Configs(
        tenant='test_tenant',
        integration_type='test_type'
    )
    await config.create_or_update()


if __name__ == '__main__':
    app_factory()
    loop = asyncio.get_event_loop()
    if sys.argv[1] == 'create':
        loop.run_until_complete(drop_all_tables())
        loop.run_until_complete(create_all_tables())
        loop.run_until_complete(fill_db_with_test_data())
    elif sys.argv[1] == 'drop':
        loop.run_until_complete(drop_all_tables())

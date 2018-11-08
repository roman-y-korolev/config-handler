import logging
import uuid

import sqlalchemy as sa
from psycopg2 import IntegrityError

from utils.database import db
from utils.password import make_hash

from models.base import BaseModel

logger = logging.getLogger(__name__)

metadata = sa.MetaData()


class Users(BaseModel):
    table = sa.Table('users', metadata,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('login', sa.String, unique=True),
                     sa.Column('password', sa.String())
                     )

    def __init__(self, login, password):
        """
        Constructor for User objects
        :param login: login
        :type login: str
        :param password: pass
        :type password: str
        """
        self.login = login
        self.password = make_hash(password)
        self.id = None

    async def create(self):
        """
        Create user in database
        :return: self or None
        :rtype: Users instance or None
        """
        try:
            query = self.table.insert().values(login=self.login, password=self.password)
            async with db['engine'].acquire() as conn:
                result = await (await conn.execute(query)).fetchone()

                self.id = result.id

                return self
        except IntegrityError:
            logger.error('User with login "{login}" can not be created'.format(login=self.login))
            return None

    @classmethod
    async def get_id(cls, login, password):
        """
        Get user_id with login and password
        :param login: login
        :type login: str
        :param password: pass
        :type password: str
        :return: users is if exists or None
        :rtype: int or None
        """
        password = make_hash(password)
        query = cls.table.select().where(sa.and_(cls.table.c.login == login, cls.table.c.password == password))
        async with db['engine'].acquire() as conn:
            result = await (await conn.execute(query)).fetchone()
            return None if not result else result.id


class Tokens(BaseModel):
    table = sa.Table('tokens', metadata,
                     sa.Column('id', sa.Integer, primary_key=True),
                     sa.Column('token', sa.String(255), unique=True),
                     sa.Column('user_id', None, sa.ForeignKey('users.id'))
                     )

    def __init__(self, user_id):
        """
        Tokens constructor
        :param user_id:
        :type user_id:
        """
        self.id = None
        self.token = str(uuid.uuid4())
        self.user_id = user_id

    async def create(self):
        """
        Create token for user in database
        :return:
        :rtype:
        """
        async with db['engine'].acquire() as conn:
            query = self.table.insert().values(token=self.token, user_id=self.user_id)
            await conn.execute(query)

    @classmethod
    async def check(cls, token):
        """
        Check if token is valid
        :param token: token
        :type token: str
        :return: False or True
        :rtype: bool
        """
        query = cls.table.select().where(cls.table.c.token == token)
        async with db['engine'].acquire() as conn:
            result = await (await conn.execute(query)).fetchone()
            return False if not result else True

import logging

import sqlalchemy as sa

from models.base import BaseModel
from utils.database import db

logger = logging.getLogger(__name__)

metadata = sa.MetaData()


class Configs(BaseModel):
    table = sa.Table('configs', metadata,
                     sa.Column('tenant', sa.String, primary_key=True),
                     sa.Column('integration_type', sa.String, primary_key=True),
                     sa.Column('username', sa.String),
                     sa.Column('password', sa.String),
                     sa.Column('session_url', sa.String),
                     sa.Column('booking_url', sa.String),
                     )

    fields = ['tenant', 'integration_type', 'username', 'password', 'session_url', 'booking_url']

    def __init__(self, tenant, integration_type, username=None, password=None, session_url=None, booking_url=None):
        self.tenant = tenant
        self.integration_type = integration_type
        self.username = username
        self.password = password
        self.session_url = session_url
        self.booking_url = booking_url

    @classmethod
    async def get(cls, tenant, integration_type):
        """
        Get config by "tenant" and "integration_type"
        :param tenant: tenant
        :type tenant: str
        :param integration_type: integration_type
        :type integration_type: str
        :return: config
        :rtype: Configs
        """
        query = cls.table.select().where(cls.table.c.tenant == tenant).where(
            cls.table.c.integration_type == integration_type)
        async with db['engine'].acquire() as conn:
            result = await (await conn.execute(query)).fetchone()

            if result:
                config = Configs(tenant=result.tenant,
                                 integration_type=result.integration_type,
                                 username=result.username,
                                 password=result.password,
                                 session_url=result.session_url,
                                 booking_url=result.booking_url)
            else:
                config = None

            return config

    async def create_or_update(self):
        """
        Update config in database or create if it not exists
        :return: None
        :rtype: None
        """
        query = self.table.select().where(self.table.c.tenant == self.tenant).where(
            self.table.c.integration_type == self.integration_type)

        async with db['engine'].acquire() as conn:
            result = await (await conn.execute(query)).fetchone()

            if not result:
                query = self.table.insert().values(**self.to_dict())

                await conn.execute(query)
                message = "Config '{tenant} : {integration_type}' is created".format(
                    tenant=self.tenant,
                    integration_type=self.integration_type)

            else:
                values = self.to_dict()
                update_values = {k: values[k] for k in values if values[k] is not None}
                query = self.table.update().where(self.table.c.tenant == self.tenant).where(
                    self.table.c.integration_type == self.integration_type).values(**update_values)

                await conn.execute(query)
                message = "Config '{tenant} : {integration_type}' is updated".format(
                    tenant=self.tenant,
                    integration_type=self.integration_type)

            logger.info(message)

            return message

    def to_formatted_dict(self):
        result = {
            "tenant": self.tenant,
            "integration_type": self.integration_type,
            "configuration": {
                "username": self.username,
                "password": self.password,
                "wsdl_urls": {
                    "session_url": self.session_url,
                    "booking_url": self.booking_url
                }
            }
        }

        return result

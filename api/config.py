import logging

from aiohttp import web
from jsonschema import validate, ValidationError

from models.config import Configs
from utils.api import get_params

from utils.api import token_required

logger = logging.getLogger(__name__)


class ConfigEndpoint:

    @classmethod
    @token_required
    async def post(cls, request):
        """
        Endpoint for recipe creation
        :param request: aiohttp request
        :type request: aiohttp.web_request.Request
        :return: json with new recipe id
        :rtype: json
        """
        schema = {
            "type": "object",
            "properties": {
                "tenant": {"type": "string"},
                "integration_type": {"type": "string"},
                "token": {"type": "string"},
                "configuration": {
                    "type": "object",
                    "properties": {
                        "username": {"type": "string"},
                        "password": {"type": "string"},
                        "wsdl_urls": {
                            "type": "object",
                            "properties": {
                                "session_url": {"type": "string"},
                                "booking_url": {"type": "string"}
                            }
                        }
                    },
                    "additionalProperties": False
                }
            },
            "additionalProperties": False,
            "required": ["tenant", "integration_type", "token"]
        }

        params = await get_params(request)
        try:
            validate(params, schema)
        except ValidationError as e:
            return web.json_response(data={'error': e.message}, status=400)

        values = dict()
        values['tenant'] = params['tenant']
        values['integration_type'] = params['integration_type']
        if 'configuration' in params:
            if 'username' in params['configuration']:
                values['username'] = params['configuration']['username']
            if 'password' in params['configuration']:
                values['password'] = params['configuration']['username']
            if 'wsdl_urls' in params['configuration']:
                if 'session_url' in params['configuration']['wsdl_urls']:
                    values['session_url'] = params['configuration']['wsdl_urls']['session_url']
                if 'booking_url' in params['configuration']['wsdl_urls']:
                    values['booking_url'] = params['configuration']['wsdl_urls']['booking_url']

        config = Configs(**values)

        message = await config.create_or_update()

        return web.json_response(data={"message": message}, status=200)

    @classmethod
    @token_required
    async def get(cls, request):

        schema = {
            "type": "object",
            "properties": {
                "tenant": {"type": "string"},
                "integration_type": {"type": "string"},
                "token": {"type": "string"},
            },
            "additionalProperties": False,
            "required": ["tenant", "integration_type", "token"]
        }

        params = await get_params(request)
        try:
            validate(params, schema)
        except ValidationError as e:
            return web.json_response(data={'error': e.message}, status=400)

        config = await Configs.get(tenant=params['tenant'], integration_type=params['integration_type'])
        if config is None:
            return web.json_response(data={'error': 'There are no configurations with the specified parameters'},
                                     status=404)
        else:
            return web.json_response(data=config.to_formatted_dict(), status=200)

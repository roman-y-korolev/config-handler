import logging

from aiohttp import web
from jsonschema import validate, ValidationError

from utils.api import get_params
from utils.authorization import authorize

logger = logging.getLogger(__name__)


class LoginEndpoint():
    @classmethod
    async def get(cls, request):
        """
        Authorization endpoint
        :param request: aiohttp request
        :type request: aiohttp.web_request.Request
        :return: token
        :rtype: json {"token":"..."}
        """
        schema = {
            "type": "object",
            "properties": {
                "login": {"type": "string"},
                "password": {"type": "string"}
            },
            "required": ["login", "password"]
        }

        params = await get_params(request)
        try:
            validate(params, schema)
        except ValidationError as e:
            return web.json_response(data={'error': e.message}, status=400)
        token = await authorize(login=params['login'], password=params['password'])

        if token is None:
            return web.json_response(
                data={"error": "incorrect login or password"},
                status=403)
        else:
            return web.json_response(
                data={"token": token},
                status=200)

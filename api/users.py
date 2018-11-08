import json

from aiohttp import web
from jsonschema import validate, ValidationError

from models.users import Users
from utils.api import get_params


class UserEndpoint:
    @classmethod
    async def post(cls, request):
        """
        Endpoint for user creation
        :param request: request
        :type request:
        :return: created user id or error
        :rtype: json
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

        user = Users(login=params['login'], password=params['password'])
        user = await user.create()

        if user is None:
            return web.json_response(
                data={"error": "User with login '{login}' can not be created".format(login=params['login'])},
                status=400)
        else:
            return web.json_response(data={"user_id": user.id}, status=200)

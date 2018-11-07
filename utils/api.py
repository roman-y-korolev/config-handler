import logging
from functools import wraps
from json.decoder import JSONDecodeError

from aiohttp import web

from models.users import Tokens
from utils.database import db

logger = logging.getLogger(__name__)


async def get_params(request):
    """
    Get parameters from request
    :param request: aiohttp request
    :type request: aiohttp.web_request.Request
    :return: dict of params
    :rtype: dict
    """
    method = request.method
    params = dict()
    if method == 'GET':
        result = request.rel_url.query
        for key in result.keys():
            params[key] = result[key]
    else:
        try:
            params = await request.json()
        except JSONDecodeError as e:
            logger.warning('There is no params or received invalid JSON')
    return params


def token_required(func):
    """
    Decorator for API methods. Check if vaid token in parameters
    :param func: method
    :type func: func
    :return: wrapper
    :rtype: func
    """

    @wraps(func)
    async def wrapper(self, request):
        params = await get_params(request)
        async with db['engine'].acquire() as conn:
            if 'token' in params and await Tokens.check(token=params['token']):
                return await func(self, request)
            else:
                return web.json_response(data={'error': "invalid token"}, status=403)

    return wrapper

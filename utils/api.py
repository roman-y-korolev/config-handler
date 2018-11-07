import logging
from json.decoder import JSONDecodeError

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

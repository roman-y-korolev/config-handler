import logging

from models.users import Users, Tokens

logger = logging.getLogger(__name__)


async def authorize(login, password):
    """
    Authorize function. Creates token and return it, if login and password was correct
    :param login: login
    :type login: str
    :param password: pass
    :type password: str
    :return: token
    :rtype: str
    """
    user_id = await Users.get_id(login=login, password=password)
    if user_id:
        token = Tokens(user_id=user_id)
        await token.create()
        return token.token
    else:
        logger.warning('incorrect login or password')
        return None

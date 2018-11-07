from aiopg.sa import create_engine

db = dict()


async def get_engine(db_config):
    """
    Get postgres engine
    :param db_config: config dict
    :type db_config: dict
    :return: aiopg engine
    :rtype: aiopg engine
    """
    engine = await create_engine(**db_config)
    return engine

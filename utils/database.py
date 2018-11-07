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


async def create_all_tables():
    """
    Create all the tables
    :return:
    :rtype:
    """
    query = """
        create table if not exists users(
            id serial PRIMARY KEY,
            login varchar unique,
            password varchar
        );
        
        create table if not exists tokens(
            id serial primary key,
            token varchar unique,
            user_id int references users(id)
        );
        
        create table if not exists configs(
            tenant varchar,
            integration_type varchar,
            username varchar,
            password varchar,
            session_url varchar,
            booking_url varchar,
            primary key(tenant, integration_type)
        );
    """
    async with db['engine'].acquire() as conn:
        await conn.execute(query)


async def drop_all_tables():
    """
    drop all the tables
    :return:
    :rtype:
    """
    query = """
        drop table if exists configs;
        drop table if exists tokens;
        drop table if exists users;
    """
    async with db['engine'].acquire() as conn:
        await conn.execute(query)

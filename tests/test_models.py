from models.config import Configs
from models.users import Users, Tokens


async def test_config_model(test_cli):
    config = Configs(tenant='1',
                     integration_type='2',
                     username='3'
                     )

    await config.create_or_update()
    config = await config.get(tenant='1', integration_type='2')
    assert config.username == '3'

    config = Configs(tenant='1',
                     integration_type='2',
                     password='4'
                     )

    await config.create_or_update()
    config = await config.get(tenant='1', integration_type='2')
    assert config.username == '3'
    assert config.password == '4'


async def test_user_model(test_cli):
    user = Users(login='test_model_login', password='test_model_password')
    user_id = await user.create()

    assert user_id is not None

    user_id = await user.create()
    assert user_id is None


async def test_token_model(test_cli):
    token = Tokens(user_id=1)

    await token.create()

    assert await Tokens.check(token.token) is True
    assert await Tokens.check('wrong-token') is False

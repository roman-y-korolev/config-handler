import json
import logging
import uuid

from models.config import Configs

logger = logging.getLogger(__name__)


async def test_create_user(test_cli):
    resp = await test_cli.post('/user')
    assert resp.status == 400
    data = {
        "login": "test_login1",
        "password": "test_password"
    }
    resp = await test_cli.post('/user', data=json.dumps(data))
    assert resp.status == 200

    resp = await test_cli.post('/user', data=json.dumps(data))
    assert resp.status == 400


async def test_login(test_cli):
    resp = await test_cli.get('/login')
    assert resp.status == 400

    data = {
        "login": "wrong_login",
        "password": "test_password"
    }
    resp = await test_cli.get('/login', params=data)
    assert resp.status == 403

    data = {
        "login": "test_login",
        "password": "test_password"
    }
    resp = await test_cli.get('/login', params=data)
    assert resp.status == 200

    text = await resp.text()
    result = json.loads(text)
    assert 'token' in result


async def test_create_config(test_cli):
    data = {
        "login": "test_login",
        "password": "test_password"
    }
    resp = await test_cli.get('/login', params=data)
    text = await resp.text()
    result = json.loads(text)
    token = result['token']

    data = {
        "integration_type": "flight-information-system",
        "token": token,
        "configuration": {
            "username": "acme_user",
            "password": "acme12345",
            "wsdl_urls": {
                "session_url": "https://session.manager.svc",
                "booking_url": "https://booking.manager.svc"
            }
        }
    }
    resp = await test_cli.post('/config', data=json.dumps(data))
    assert resp.status == 400

    tenant = str(uuid.uuid4())
    data = {
        "tenant": tenant,
        "integration_type": "flight-information-system",
        "token": token,
        "configuration": {
            "username": "acme_user",
            "password": "acme12345",
            "wsdl_urls": {
                "session_url": "https://session.manager.svc",
                "booking_url": "https://booking.manager.svc"
            }
        }
    }
    resp = await test_cli.post('/config', data=json.dumps(data))
    assert resp.status == 200

    text = await resp.text()
    result = json.loads(text)
    assert 'created' in result['message']

    config = await Configs.get(tenant=tenant, integration_type="flight-information-system")
    assert config is not None

    data = {
        "tenant": tenant,
        "integration_type": "flight-information-system",
        "token": token,
        "configuration": {
            "username": "new_user_name"
        }
    }

    resp = await test_cli.post('/config', data=json.dumps(data))
    assert resp.status == 200

    text = await resp.text()
    result = json.loads(text)
    assert 'updated' in result['message']

    config = await Configs.get(tenant=tenant, integration_type="flight-information-system")
    assert config.username == 'new_user_name'


async def test_get_config(test_cli):
    data = {
        "login": "test_login",
        "password": "test_password"
    }
    resp = await test_cli.get('/login', params=data)
    text = await resp.text()
    result = json.loads(text)
    token = result['token']

    data = {
        "integration_type": "flight-information-system",
        "token": token
    }
    resp = await test_cli.get('/config', params=data)
    assert resp.status == 400

    tenant = str(uuid.uuid4())
    data = {
        "tenant": tenant,
        "integration_type": "flight-information-system",
        "token": token
    }
    resp = await test_cli.get('/config', params=data)
    assert resp.status == 404

    values = {
        "tenant": tenant,
        "integration_type": "flight-information-system",
        "username": "new_user_name",
        "password": "new_pass"
    }
    config = Configs(**values)
    await config.create_or_update()

    resp = await test_cli.get('/config', params=data)
    assert resp.status == 200

    text = await resp.text()
    result = json.loads(text)
    assert result['configuration']['username'] == 'new_user_name'


async def test_token(test_cli):
    data = {
        "login": "test_login",
        "password": "test_password"
    }
    resp = await test_cli.get('/login', params=data)
    text = await resp.text()
    result = json.loads(text)
    token = result['token']

    data = {
        "tenant": "test_tenant",
        "integration_type": "test_type",
        "token": token
    }
    resp = await test_cli.get('/config', params=data)
    assert resp.status == 200

    data = {
        "tenant": "test_tenant",
        "integration_type": "test_type"
    }
    resp = await test_cli.get('/config', params=data)
    assert resp.status == 403

    data = {
        "tenant": "test_tenant",
        "integration_type": "test_type",
        "token": "wrong_token"
    }
    resp = await test_cli.get('/config', params=data)
    assert resp.status == 403

import json
import logging
import uuid

from models.config import Configs

logger = logging.getLogger(__name__)

token = None


async def test_create_config(test_cli):
    tenant = str(uuid.uuid4())
    data = {
        "tenant": tenant,
        "integration_type": "flight-information-system",
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
    tenant = str(uuid.uuid4())
    data = {
        "tenant": tenant,
        "integration_type": "flight-information-system"
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

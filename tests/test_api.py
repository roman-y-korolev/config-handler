import json
import uuid

from models.config import Configs

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

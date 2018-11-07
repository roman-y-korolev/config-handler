import pytest

from utils.factory import app_factory


@pytest.yield_fixture
def app():
    app = app_factory()
    yield app


@pytest.fixture
def test_cli(loop, app, aiohttp_client):
    return loop.run_until_complete(aiohttp_client(app))

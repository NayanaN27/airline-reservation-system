import pytest
from app import create_app

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,  # disable CSRF for tests (safe for test env)
    )
    return app

@pytest.fixture()
def client(app):
    return app.test_client()
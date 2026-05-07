import os
import subprocess
import pymysql.cursors
import pytest



# Make the app use the same DB as reset_test_db.py
os.environ["DB_HOST"] = os.environ.get("TEST_DB_HOST", "localhost")
os.environ["DB_USER"] = os.environ.get("TEST_DB_USER", "airuser")
os.environ["DB_PASSWORD"] = os.environ.get("TEST_DB_PASSWORD", "StrongPassword123!")
os.environ["DB_NAME"] = os.environ.get("TEST_DB_NAME", "air")

# Prevent DATABASE_URL from overriding DB_*
os.environ.pop("DATABASE_URL", None)

from app import create_app

def get_test_db():
    return pymysql.connect(
        host=os.getenv("TEST_DB_HOST", "localhost"),
        user=os.getenv("TEST_DB_USER", "airuser"),
        password=os.getenv("TEST_DB_PASSWORD", "StrongPassword123!"),
        database=os.getenv("TEST_DB_NAME", "air"),
        cursorclass=pymysql.cursors.DictCursor,
    )

@pytest.fixture(scope="session", autouse=True)
def reset_test_db():
    subprocess.check_call(["python", "scripts/reset_test_db.py"])
    yield

@pytest.fixture()
def app():
    app = create_app()
    app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)

    host = os.getenv("TEST_DB_HOST", "localhost")
    user = os.getenv("TEST_DB_USER", "airuser")
    pwd  = os.getenv("TEST_DB_PASSWORD", "StrongPassword123!")
    db   = os.getenv("TEST_DB_NAME", "air")

    # app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{user}:{pwd}@{host}/{db}"
    app.config["GET_DB"] = get_test_db
    return app

@pytest.fixture()
def client(app):
    return app.test_client()
import pytest
from time import sleep

@pytest.fixture
def api_base_url():
    return "https://example.test/api"

# Put common fixtures in tests/conftest.py. Pytest auto-discovers it—no imports needed.\

# Return a function from the fixture to build resources with different args.

@pytest.fixture
def user_factory():
    def _make_user(id=1, name="Lakshay", role="tester"):
        return {"id": id, "name": name, "role": role}
    return _make_user

@pytest.fixture(scope="session")
def db_session(scope="session"):
    # start db
    db = object()
    yield db
    #teardown

@pytest.fixture
def db_cursor(db_session):
    # return a transaction or cursor derived from db_session
    return {"cursor": True}

# Fixtures can depend on other fixtures via parameters.

@pytest.fixture
def token():
    return "secret-token"

@pytest.fixture
def client(token, api_base_url):
    class Client:
        def __init__(self, base, tok):
            self.base = base
            self.tok = tok
    return Client(api_base_url, token)


import pytest

from src import app


@pytest.fixture
def client():
    with app.app.test_client() as client:
        yield client


def test_hello(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.data == b"Hello, World!"

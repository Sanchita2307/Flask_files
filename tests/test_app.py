import pytest
from docker_flask.app import app as flask_app


@pytest.fixture
def client():
    return flask_app.test_client()


def test_home_status_code(client):
    """Root endpoint should return HTTP 200"""
    resp = client.get("/")
    assert resp.status_code == 200


def test_home_json_message(client):
    """Root endpoint should return expected JSON message"""
    resp = client.get("/")
    assert resp.is_json
    assert resp.get_json() == {"message": "Hi from docker flask, Sanchita, How're you ?"}


def test_404_for_unknown_route(client):
    """Unknown routes should return 404"""
    resp = client.get("/this-route-does-not-exist")
    assert resp.status_code == 404

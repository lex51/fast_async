from starlette.testclient import TestClient
import json

from src.main import app

client = TestClient(app)


def test_ping():
    """
    simplest test"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert response.json() == {"api_version": "0.1", "ok": True, "data": "pong!"}


def test_invalid_record():
    """
    have invalid mail or uuid or both
    """
    response = client.post(
        "/save_mail",
        data=json.dumps(
            {"email": "err_mail.com", "uuid": "15303cf4-9afb-4dcf-b6b2-f2775ea42ef1"}
        ),
    )
    assert response.status_code == 422
    assert response.json()["ok"] == False
    assert len(response.json()["data"]["error"]) == 1

    response = client.post(
        "/save_mail",
        data=json.dumps(
            {"email": "user@example.com", "uuid": "15303cf4-9afb-4dcf-b6b2-f2775111111"}
        ),
    )
    assert response.status_code == 422
    assert response.json()["ok"] == False
    assert len(response.json()["data"]["error"]) == 1

    response = client.post(
        "/save_mail",
        data=json.dumps(
            {"email": "err_mail.com", "uuid": "303cf4-9afb-4dcf-b6b2-f2775e11111"}
        ),
    )
    assert response.status_code == 422
    assert response.json()["ok"] == False
    assert len(response.json()["data"]["error"]) == 2


def test_valid_record():
    """
    good record
    """

    response = client.post(
        "/save_mail",
        data=json.dumps(
            {
                "email": "user@example.com",
                "uuid": "5b80f47c-951b-4979-9c81-1fa5544d63d5",
            }
        ),
    )
    assert response.status_code == 201
    assert response.json()["ok"] == True
    assert response.json()["data"]["email"] == "user@example.com"
    assert response.json()["data"]["uuid"] == "5b80f47c-951b-4979-9c81-1fa5544d63d5"
    assert type(response.json()["data"]["id"]) == int

""" 
    Main test suite for plotlib
    Philip Suggars
    Red Robot Labs - Dec 2021
"""

import pytest
from fastapi.testclient import TestClient
from api.api import app
from api.api import VERSION

# from fastapi.encoders import jsonable_encoder

# set up fastAPI app for testing
client = TestClient(app)


# ------------------------
#     API route tests
# ------------------------


@pytest.mark.asyncio
def test_post():
    """test posting a prompt to API"""
    data = {"prompt": "prompted thing", "temperature": 0.7}
    response = client.post("/", json=data)
    assert response.status_code == 200
    assert response.json()["data"]["text"] == data["prompt"]


@pytest.mark.asyncio
def test_root_path():
    """return version number"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["data"]["version"] == VERSION
    assert response.json()["message"] == "Success"

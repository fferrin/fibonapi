from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


class TestFibonacciEndpoints:
    @staticmethod
    def test_get_bonacci_by_number():
        response = client.get("/api/fibonacci/30")
        assert response.status_code == 200
        assert response.json() == {"data": {"value": 832_040}}

    @staticmethod
    def test_get_bonacci_by_number_invalid_value():
        response = client.get("/api/fibonacci/-234")
        assert response.status_code == 400
        assert response.json() == {
            "detail": "Number must be non negative. Received: -234"
        }

    @staticmethod
    def test_get_bonacci_by_number_non_numeric_value():
        response = client.get("/api/fibonacci/foo")
        assert response.status_code == 422

    @staticmethod
    def test_get_bonacci_by_range():
        response = client.get("/api/fibonacci/0/to/6")
        assert response.status_code == 200
        assert response.json() == {"data": {"value": [0, 1, 1, 2, 3, 5]}}

    @staticmethod
    def test_blacklist_by_number():
        response = client.post("/api/fibonacci/0/blacklist")
        assert response.status_code == 204

    @staticmethod
    def test_whitelist_by_number():
        response = client.post("/api/fibonacci/0/whitelist")
        assert response.status_code == 204

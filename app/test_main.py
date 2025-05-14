import pytest
from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


class TestFibonacciEndpoints:
    @staticmethod
    @pytest.mark.parametrize(
        ("method", "endpoint"),
        (
            ("GET", "/api/fibonacci/-1"),
            ("GET", "/api/fibonacci/-1/to/6"),
            ("GET", "/api/fibonacci/0/to/-1"),
            ("POST", "/api/fibonacci/-1/blacklist"),
            ("POST", "/api/fibonacci/-1/whitelist"),
        ),
    )
    def test_fibonacci_numbers_must_be_non_negatives(method, endpoint):
        action = getattr(client, method.lower())
        response = action(endpoint)

        content = response.json()["detail"][0]
        assert response.status_code == 422
        assert content["msg"] == "Input should be greater than or equal to 0"
        assert content["input"] == "-1"

    @staticmethod
    @pytest.mark.parametrize(
        ("method", "endpoint"),
        (
            ("GET", "/api/fibonacci/foobar"),
            ("GET", "/api/fibonacci/foobar/to/6"),
            ("GET", "/api/fibonacci/0/to/foobar"),
            ("POST", "/api/fibonacci/foobar/blacklist"),
            ("POST", "/api/fibonacci/foobar/whitelist"),
        ),
    )
    def test_fibonacci_numbers_must_be_numbers(method, endpoint):
        action = getattr(client, method.lower())
        response = action(endpoint)

        content = response.json()["detail"][0]
        assert response.status_code == 422
        assert (
            content["msg"]
            == "Input should be a valid integer, unable to parse string as an integer"
        )
        assert content["input"] == "foobar"

    class TestByNumber:
        @staticmethod
        def test_get_bonacci_by_number():
            response = client.get("/api/fibonacci/30")
            assert response.status_code == 200
            assert response.json() == {
                "data": {
                    "number": 30,
                    "value": 832_040,
                }
            }

    class TestByRange:
        @staticmethod
        def test_get_bonacci_by_range():
            response = client.get("/api/fibonacci/0/to/6")
            assert response.status_code == 200
            assert response.json() == {
                "data": {
                    "values": [0, 1, 1, 2, 3, 5],
                },
                "metadata": None,
            }

    class TestWhiteAndBlacklist:
        @staticmethod
        def test_blacklist_by_number():
            response = client.post("/api/fibonacci/0/blacklist")
            assert response.status_code == 204

        @staticmethod
        def test_whitelist_by_number():
            response = client.post("/api/fibonacci/0/whitelist")
            assert response.status_code == 204

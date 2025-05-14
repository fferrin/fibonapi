import pytest
from fastapi.testclient import TestClient

from .main import app
from .fibonacci import FibonacciService


client = TestClient(app)


class TestFibonacciEndpoints:
    class TestInputValidations:
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

    class TestEndpointsResults:
        @staticmethod
        def test_get_fibonacci_by_number():
            response = client.get("/api/fibonacci/30")

            assert response.status_code == 200
            assert response.json() == {
                "data": {
                    "number": 30,
                    "value": 832_040,
                }
            }

        @staticmethod
        def test_get_fibonacci_by_range():
            response = client.get("/api/fibonacci/0/to/6")

            assert response.status_code == 200
            assert response.json() == {
                "data": {
                    "values": [0, 1, 1, 2, 3, 5],
                },
            }

        @staticmethod
        def test_blacklist_by_number():
            response = client.post("/api/fibonacci/0/blacklist")

            assert response.status_code == 204

        @staticmethod
        def test_whitelist_by_number():
            response = client.post("/api/fibonacci/0/whitelist")

            assert response.status_code == 204

    class TestListWithPagination:
        fibo_service = FibonacciService()

        def test_get_fibonacci_defaults(self):
            response = client.get("/api/fibonacci/")

            assert response.status_code == 200
            content = response.json()
            assert len(content["data"]["values"]) == 100
            assert content["data"]["values"] == self.fibo_service.by_range(0, 100)
            assert content["metadata"] == {
                "page": 1,
                "page_size": 100,
                "next": "/api/fibonacci/?page=2&page_size=100",
            }

        def test_get_fibonacci_page_size(self):
            response = client.get("/api/fibonacci/?page_size=5")

            assert response.status_code == 200
            content = response.json()
            assert len(content["data"]["values"]) == 5
            assert content["data"]["values"] == self.fibo_service.by_range(0, 5)
            assert content["metadata"] == {
                "page": 1,
                "page_size": 5,
                "next": "/api/fibonacci/?page=2&page_size=5",
            }

        def test_get_fibonacci_page(self):
            response = client.get("/api/fibonacci/?page=10&page_size=5")

            assert response.status_code == 200
            content = response.json()
            assert len(content["data"]["values"]) == 5
            assert content["data"]["values"] == self.fibo_service.by_range(45, 50)
            assert content["metadata"] == {
                "page": 10,
                "page_size": 5,
                "next": "/api/fibonacci/?page=11&page_size=5",
            }

        def test_get_fibonacci_next(self):
            response = client.get("/api/fibonacci/?page=10&page_size=5")
            content = response.json()
            assert content["data"]["values"] == self.fibo_service.by_range(45, 50)

            response = client.get(content["metadata"]["next"])

            content = response.json()
            assert content["data"]["values"] == self.fibo_service.by_range(50, 55)

        def test_get_fibonacci_with_black_and_whitelist(self):
            url = "/api/fibonacci/?page=10&page_size=5"

            # No blacklisted
            response = client.get(url)

            assert response.status_code == 200
            values = response.json()["data"]["values"]
            assert len(values) == 5
            assert values == self.fibo_service.by_range(45, 50)

            # Blacklist n = 45
            response = client.post("/api/fibonacci/45/blacklist")
            assert response.status_code == 204

            # Check list again
            response = client.get(url)

            assert response.status_code == 200
            values = response.json()["data"]["values"]
            assert len(values) == 4
            assert values == self.fibo_service.by_range(46, 50)

            # Whitelist n = 45 again
            response = client.post("/api/fibonacci/45/whitelist")
            assert response.status_code == 204

            # Check list again
            response = client.get(url)

            assert response.status_code == 200
            values = response.json()["data"]["values"]
            assert len(values) == 5
            assert values == self.fibo_service.by_range(45, 50)

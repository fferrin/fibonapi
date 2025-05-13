from fastapi.testclient import TestClient

from .main import app


client = TestClient(app)


class TestFibonacciEndpoints:
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

        @staticmethod
        def test_get_bonacci_by_number_invalid_value():
            response = client.get("/api/fibonacci/-1")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Number must be non negative. Received: -1"
            }

        @staticmethod
        def test_get_bonacci_by_number_non_numeric_value():
            response = client.get("/api/fibonacci/foo")
            assert response.status_code == 422

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

        @staticmethod
        def test_with_number_invalid_value():
            response = client.get("/api/fibonacci/-1/to/6")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Number must be non negative. Received: -1"
            }

        @staticmethod
        def test_non_numeric_value():
            response = client.get("/api/fibonacci/foo/to/6")
            assert response.status_code == 422

    class TestWhiteAndBlacklist:
        @staticmethod
        def test_blacklist_by_number():
            response = client.post("/api/fibonacci/0/blacklist")
            assert response.status_code == 204

        @staticmethod
        def test_blacklist_with_number_invalid_value():
            response = client.post("/api/fibonacci/-1/blacklist")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Number must be non negative. Received: -1"
            }

        @staticmethod
        def test_blacklist_non_numeric_value():
            response = client.post("/api/fibonacci/foo/blacklist")
            assert response.status_code == 422

        @staticmethod
        def test_whitelist_by_number():
            response = client.post("/api/fibonacci/0/whitelist")
            assert response.status_code == 204

        @staticmethod
        def test_whitelist_with_number_invalid_value():
            response = client.post("/api/fibonacci/-1/whitelist")
            assert response.status_code == 400
            assert response.json() == {
                "detail": "Number must be non negative. Received: -1"
            }

        @staticmethod
        def test_whitelist_non_numeric_value():
            response = client.post("/api/fibonacci/foo/whitelist")
            assert response.status_code == 422

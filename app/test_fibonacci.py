import pytest

from fibonacci import FibonacciService


class TestFibonacciService:
    @staticmethod
    @pytest.mark.parametrize(
        ("n", "result"),
        (
            (0, 0),
            (1, 1),
            (2, 1),
            (3, 2),
            (4, 3),
            (5, 5),
            (30, 832_040),
            (100, 354_224_848_179_261_915_075),
        ),
    )
    def test_by_number(n, result):
        fibo = FibonacciService()
        assert fibo.by_number(n) == result

    @staticmethod
    def test_numbers_are_stored():
        fibo = FibonacciService()
        assert len(fibo.numbers) == 2

        fibo.by_number(10)
        # Fibonacci numbers start from 0
        assert len(fibo.numbers) == 10 + 1

        # Bigger number increase the values stored
        fibo.by_number(30)
        assert len(fibo.numbers) == 30 + 1
        # Querying for the max value does not increase the size
        fibo.by_number(30)
        assert len(fibo.numbers) == 30 + 1

    @staticmethod
    @pytest.mark.parametrize(
        ("from_", "to", "result"),
        (
            (0, 1, [0]),
            (0, 6, [0, 1, 1, 2, 3, 5]),
        ),
    )
    def test_by_range(from_, to, result):
        fibo = FibonacciService()
        assert fibo.by_range(from_, to) == result

    @staticmethod
    def test_blacklist_by_number():
        fibo = FibonacciService()
        assert fibo.by_number(2) == 1
        assert fibo.by_range(0, 6) == [0, 1, 1, 2, 3, 5]

        fibo.blacklist_by_number(2)

        assert fibo.by_number(2) is None
        assert fibo.by_range(0, 6) == [0, 1, 2, 3, 5]

    @staticmethod
    def test_whitelist_by_number():
        fibo = FibonacciService()
        fibo.blacklist_by_number(5)
        assert fibo.by_number(5) is None
        assert fibo.by_range(0, 6) == [0, 1, 1, 2, 3]

        fibo.whitelist_by_number(5)

        assert fibo.by_number(5) == 5
        assert fibo.by_range(0, 6) == [0, 1, 1, 2, 3, 5]

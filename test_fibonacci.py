import pytest

from fibonacci import fibonacci


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
def test_compute_fibonacci(n, result):
    assert fibonacci(n) == result

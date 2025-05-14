from typing import List, Optional


class FibonacciService:
    def __init__(self):
        self._numbers = [0, 1]
        self._blacklisted = set()

    def by_number(self, n: int) -> Optional[int]:
        if n in self._blacklisted:
            return None

        if n >= len(self._numbers):
            self._fill_up_to(n)

        return self._numbers[n]

    def by_range(self, from_: int, to: int) -> List[int]:
        if to >= len(self._numbers):
            self._fill_up_to(to)

        return [
            self._numbers[idx]
            for idx in range(from_, to)
            if idx not in self._blacklisted
        ]

    def blacklist_by_number(self, n: int) -> None:
        self._blacklisted.add(n)

    def whitelist_by_number(self, n: int) -> None:
        self._blacklisted.remove(n)

    def _fill_up_to(self, to: int) -> None:
        new_numbers = []
        a, b = self._numbers[-2], self._numbers[-1]
        for _ in range(len(self._numbers), to + 1):
            a, b = b, a + b
            new_numbers.append(b)

        self._numbers.extend(new_numbers)

    @property
    def numbers(self) -> List[int]:
        return self._numbers

from typing import Callable

CLOCK_FUNC = Callable[[], float]


def now() -> CLOCK_FUNC: ...

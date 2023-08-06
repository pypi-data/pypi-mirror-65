from __future__ import annotations

from typing import TypeVar
from typing import Union

from hypothesis.strategies import just
from hypothesis.strategies import sampled_from
from hypothesis.strategies import SearchStrategy


T = TypeVar("T")


def maybe_just(x: T) -> Union[T, SearchStrategy[T]]:
    """Strategy generating `x` or `just(x)`."""

    return sampled_from([x, just(x)])

from __future__ import annotations

from typing import Callable
from typing import cast
from typing import Dict
from typing import Tuple

import hypothesis
from functional_itertools import CDict
from functional_itertools import CList
from hypothesis.strategies import data
from hypothesis.strategies import DataObject
from hypothesis.strategies import dictionaries
from hypothesis.strategies import integers
from hypothesis.strategies import lists
from hypothesis.strategies import text

from hypothesis_pandas.draw_if import draw_if_args
from hypothesis_pandas.draw_if import draw_if_kwargs
from tests.testing import maybe_just


given = cast(Callable[..., Callable[[Callable[..., None]], Callable[..., None]]], hypothesis.given)


@given(data=data(), args=lists(integers()))
def test_draw_if_args(data: DataObject, args: Tuple[int, ...]) -> None:
    ints_or_strategies = []
    for arg in args:
        ints_or_strategies.append(data.draw(maybe_just(arg)))
    drawn = data.draw(draw_if_args(*ints_or_strategies))
    assert isinstance(drawn, CList)
    assert drawn == args


@given(data=data(), kwargs=dictionaries(text(), integers()))
def test_draw_if_kwargs(data: DataObject, kwargs: Dict[str, int]) -> None:
    ints_or_strategies = {}
    for key, value in kwargs.items():
        ints_or_strategies[key] = data.draw(maybe_just(value))
    drawn = data.draw(draw_if_kwargs(**ints_or_strategies))
    assert isinstance(drawn, CDict)
    assert drawn == kwargs

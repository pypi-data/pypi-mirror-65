from __future__ import annotations

from dataclasses import dataclass
from dataclasses import replace
from operator import attrgetter
from typing import Any
from typing import Callable
from typing import Generic
from typing import Tuple
from typing import TypeVar
from typing import Union

from functional_itertools import CDict
from functional_itertools import CList
from hypothesis.strategies import fixed_dictionaries
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import tuples


T = TypeVar("T")


def _is_ss(x: Any) -> bool:
    return isinstance(x, SearchStrategy)


def _not_ss(x: Any) -> bool:
    return not _is_ss(x)


@dataclass
class _Pair(Generic[T]):
    index: int
    value: Union[T, SearchStrategy[T]]


_get_index = attrgetter("index")
_get_value = attrgetter("value")


def draw_if_args(*args: Union[T, SearchStrategy[T]]) -> SearchStrategy[CList[T]]:
    """Strategy drawing from args when necessary."""

    pairs = CList(args).enumerate().starmap(_Pair)
    strat_pairs = pairs.filter(lambda x: _is_ss(x.value))
    value_pairs = pairs.filter(lambda x: _not_ss(x.value))

    def inner(x: Tuple[T, ...]) -> CList[T]:
        return (
            strat_pairs.zip(x)
            .map(lambda pair: replace(pair[0], value=pair[1]))
            .chain(value_pairs)
            .sorted(key=_get_index)
            .map(_get_value)
        )

    return tuples(*strat_pairs.map(_get_value)).map(inner)


def draw_if_kwargs(**kwargs: Union[T, SearchStrategy[T]]) -> SearchStrategy[CDict[str, T]]:
    """Strategy drawing from kwargs when necessary."""

    mapping = CDict(kwargs)
    strat_mappings = mapping.filter_values(_is_ss)
    value_mappings = mapping.filter_values(_not_ss)

    def inner(x: CDict[str, Any]) -> CDict[str, T]:
        return CDict({**x, **value_mappings})

    return fixed_dictionaries(strat_mappings).map(inner)


def draw_if(
    *args: Union[T, SearchStrategy[T]], **kwargs: Union[T, SearchStrategy[T]],
) -> SearchStrategy[Tuple[CList[T], CDict[str, T]]]:
    """Strategy drawing from args/kwargs when necessary."""

    return tuples(draw_if_args(*args), draw_if_kwargs(**kwargs))


def draw_if_map(func: Callable[..., T], *args: Any, **kwargs: Any) -> SearchStrategy[T]:
    """Strategy drawing from args/kwargs when necessary, and then mapping them into a function."""

    def inner(x: Tuple[CList[Any], CDict[str, Any]]) -> T:
        inner_args, inner_kwargs = x
        return func(*inner_args, **inner_kwargs)

    return draw_if(*args, **kwargs).map(inner)


def draw_if_flatmap(
    func: Callable[..., SearchStrategy[T]], *args: Any, **kwargs: Any,
) -> SearchStrategy[T]:
    """Strategy drawing from args/kwargs when necessary, and then flatmapping them into a strategy."""

    def inner(x: Tuple[CList[Any], CDict[str, Any]]) -> SearchStrategy[T]:
        inner_args, inner_kwargs = x
        return func(*inner_args, **inner_kwargs)

    return draw_if(*args, **kwargs).flatmap(inner)

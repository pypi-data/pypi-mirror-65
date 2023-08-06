from __future__ import annotations

from string import ascii_uppercase
from typing import Hashable
from typing import Tuple
from typing import TypeVar
from typing import Union

import numpy as np
from hypothesis import assume
from hypothesis.extra.numpy import array_shapes
from hypothesis.extra.numpy import arrays as _arrays
from hypothesis.extra.numpy import scalar_dtypes
from hypothesis.strategies import integers
from hypothesis.strategies import none
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import text
from numpy import dtype
from numpy import issubdtype
from numpy import ndarray
from pandas import DataFrame
from pandas import Index
from pandas import RangeIndex
from pandas import Series
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime  # noqa: WPS436

from hypothesis_pandas.draw_if import draw_if_flatmap
from hypothesis_pandas.draw_if import draw_if_map


Shape = Union[int, Tuple[int, ...]]
T = TypeVar("T")
DTYPES = scalar_dtypes().filter(
    lambda x: not issubdtype(x, dtype("datetime64")) and not issubdtype(x, dtype("timedelta64")),
)
LENGTHS = integers(0, 10)
NAMES = none() | text(alphabet=ascii_uppercase)
SHAPES = array_shapes()


def arrays(
    *,
    dtypes: Union[dtype, SearchStrategy[dtype]] = DTYPES,
    shapes: Union[Shape, SearchStrategy[Shape]] = SHAPES,
) -> SearchStrategy[ndarray]:
    """Strategy for generating arrays."""

    def inner(dtype: dtype, shape: Shape) -> SearchStrategy[ndarray]:
        return _arrays(dtype, shape)

    return draw_if_flatmap(inner, dtypes, shapes)


def range_indices(
    lengths: Union[int, SearchStrategy[int]] = LENGTHS,
    names: Union[Hashable, SearchStrategy[Hashable]] = NAMES,
) -> SearchStrategy[RangeIndex]:
    """Strategy for generating range indices."""

    return draw_if_map(RangeIndex, lengths, name=names)


RANGE_INDICES = range_indices()


def series(
    *,
    dtypes: Union[dtype, SearchStrategy[dtype]] = DTYPES,
    indices: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
    names: Union[Hashable, SearchStrategy[Hashable]] = NAMES,
) -> SearchStrategy[Series]:
    """Strategy for generating series."""

    def inner(dtype: np.dtype, index: Index, name: Hashable) -> SearchStrategy[Series]:
        return draw_if_map(inner2, arrays(dtypes=dtype, shapes=len(index)), index, dtype, name)

    def inner2(array: ndarray, index: Index, dtype: np.dtype, name: Hashable) -> Series:
        try:
            return Series(data=array, index=index, dtype=dtype, name=name)
        except OutOfBoundsDatetime:
            assume(False)

    return draw_if_flatmap(inner, dtypes, indices, names)


def dataframes(
    *,
    dtypes: Union[dtype, SearchStrategy[dtype]] = DTYPES,
    indices: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
    columns: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
) -> SearchStrategy[DataFrame]:
    """Strategy for generating dataframes."""

    def inner(dtype: np.dtype, index: Index, columns: Index) -> SearchStrategy[DataFrame]:
        return draw_if_map(
            inner2, arrays(dtypes=dtype, shapes=(len(index), len(columns))), index, columns, dtype,
        )

    def inner2(array: ndarray, index: Index, columns: Index, dtype: np.dtype) -> DataFrame:
        try:
            return DataFrame(data=array, index=index, columns=columns, dtype=dtype)
        except OutOfBoundsDatetime:
            assume(False)

    return draw_if_flatmap(inner, dtypes, indices, columns)

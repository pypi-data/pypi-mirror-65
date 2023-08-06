from __future__ import annotations

from string import ascii_uppercase
from typing import Hashable
from typing import Union

from hypothesis import assume
from hypothesis.extra.numpy import scalar_dtypes
from hypothesis.strategies import integers
from hypothesis.strategies import none
from hypothesis.strategies import SearchStrategy
from hypothesis.strategies import text
from hypothesis_auto_draw import auto_draw_flatmap
from hypothesis_auto_draw import auto_draw_map
from hypothesis_numpy import arrays
from numpy import dtype
from numpy import issubdtype
from numpy import ndarray
from pandas import DataFrame
from pandas import Index
from pandas import RangeIndex
from pandas import Series
from pandas._libs.tslibs.np_datetime import OutOfBoundsDatetime  # : WPS436


DTypeInput = Union[type, dtype]
DTYPES = scalar_dtypes().filter(
    lambda x: not issubdtype(x, dtype("datetime64")) and not issubdtype(x, dtype("timedelta64")),
)
LENGTHS = integers(0, 10)
NAMES = none() | text(alphabet=ascii_uppercase)


def range_indices(
    lengths: Union[int, SearchStrategy[int]] = LENGTHS,
    names: Union[Hashable, SearchStrategy[Hashable]] = NAMES,
) -> SearchStrategy[RangeIndex]:
    return auto_draw_map(RangeIndex, lengths, name=names)


RANGE_INDICES = range_indices()


def series(
    *,
    dtypes: Union[DTypeInput, SearchStrategy[DTypeInput]] = DTYPES,
    indices: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
    names: Union[Hashable, SearchStrategy[Hashable]] = NAMES,
) -> SearchStrategy[Series]:
    def inner(dtype: DTypeInput, index: Index, name: Hashable) -> SearchStrategy[Series]:
        return auto_draw_map(inner2, arrays(dtypes=dtype, shapes=len(index)), index, dtype, name)

    def inner2(array: ndarray, index: Index, dtype: DTypeInput, name: Hashable) -> Series:
        try:
            return Series(data=array, index=index, dtype=dtype, name=name)
        except OutOfBoundsDatetime:
            assume(False)

    return auto_draw_flatmap(inner, dtypes, indices, names)


def dataframes(
    *,
    dtypes: Union[DTypeInput, SearchStrategy[DTypeInput]] = DTYPES,
    indices: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
    columns: Union[Index, SearchStrategy[Index]] = RANGE_INDICES,
) -> SearchStrategy[DataFrame]:
    def inner(dtype: DTypeInput, index: Index, columns: Index) -> SearchStrategy[DataFrame]:
        return auto_draw_map(
            inner2, arrays(dtypes=dtype, shapes=(len(index), len(columns))), index, columns, dtype,
        )

    def inner2(array: ndarray, index: Index, columns: Index, dtype: DTypeInput) -> DataFrame:
        try:
            return DataFrame(data=array, index=index, columns=columns, dtype=dtype)
        except OutOfBoundsDatetime:
            assume(False)

    return auto_draw_flatmap(inner, dtypes, indices, columns)

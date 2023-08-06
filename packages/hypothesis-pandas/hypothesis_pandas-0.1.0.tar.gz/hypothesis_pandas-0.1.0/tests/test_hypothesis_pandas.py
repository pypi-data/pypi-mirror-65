from __future__ import annotations

from typing import Callable
from typing import cast
from typing import Hashable

import hypothesis
import numpy as np
from hypothesis.strategies import data
from hypothesis.strategies import DataObject
from numpy.core.records import ndarray
from pandas import DataFrame
from pandas import Index
from pandas import RangeIndex
from pandas import Series
from pandas.testing import assert_index_equal

from hypothesis_pandas import range_indices
from hypothesis_pandas.hypothesis_pandas import arrays
from hypothesis_pandas.hypothesis_pandas import dataframes
from hypothesis_pandas.hypothesis_pandas import DTYPES
from hypothesis_pandas.hypothesis_pandas import LENGTHS
from hypothesis_pandas.hypothesis_pandas import NAMES
from hypothesis_pandas.hypothesis_pandas import RANGE_INDICES
from hypothesis_pandas.hypothesis_pandas import series
from hypothesis_pandas.hypothesis_pandas import Shape
from hypothesis_pandas.hypothesis_pandas import SHAPES
from tests.testing import maybe_just


given = cast(Callable[..., Callable[[Callable[..., None]], Callable[..., None]]], hypothesis.given)


@given(data=data(), dtype=DTYPES, shape=SHAPES)
def test_arrays(data: DataObject, dtype: np.dtype, shape: Shape) -> None:
    array = data.draw(
        arrays(dtypes=data.draw(maybe_just(dtype)), shapes=data.draw(maybe_just(shape))),
    )
    assert isinstance(array, ndarray)
    assert array.dtype == dtype
    assert array.shape == shape


@given(data=data(), length=LENGTHS, name=NAMES)
def test_range_indices(data: DataObject, length: int, name: Hashable) -> None:
    index = data.draw(
        range_indices(lengths=data.draw(maybe_just(length)), names=data.draw(maybe_just(name))),
    )
    assert isinstance(index, RangeIndex)
    assert len(index) == length
    assert index.name == name


@given(data=data(), dtype=DTYPES, index=RANGE_INDICES, name=NAMES)
def test_series(data: DataObject, dtype: np.dtype, index: Index, name: Hashable) -> None:
    sr = data.draw(
        series(
            dtypes=data.draw(maybe_just(dtype)),
            indices=data.draw(maybe_just(index)),
            names=data.draw(maybe_just(name)),
        ),
    )
    assert isinstance(sr, Series)
    assert sr.dtype == dtype
    assert_index_equal(sr.index, index)
    assert sr.name == name


@given(data=data(), dtype=DTYPES, index=RANGE_INDICES, columns=RANGE_INDICES)
def test_dataframes(data: DataObject, dtype: np.dtype, index: Index, columns: Index) -> None:
    df = data.draw(
        dataframes(
            dtypes=data.draw(maybe_just(dtype)),
            indices=data.draw(maybe_just(index)),
            columns=data.draw(maybe_just(columns)),
        ),
    )
    assert isinstance(df, DataFrame)
    assert (df.dtypes == dtype).all()
    assert_index_equal(df.index, index)
    assert_index_equal(df.columns, columns)

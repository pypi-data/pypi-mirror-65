"""Hypothesis strategies for pandas objects."""
from __future__ import annotations

from hypothesis_pandas.draw_if import draw_if_flatmap
from hypothesis_pandas.draw_if import draw_if_map
from hypothesis_pandas.hypothesis_pandas import dataframes
from hypothesis_pandas.hypothesis_pandas import range_indices
from hypothesis_pandas.hypothesis_pandas import series


__all__ = [
    "draw_if_flatmap",
    "draw_if_map",
    "dataframes",
    "range_indices",
    "series",
]
__version__ = "0.2.0"

from typing import Callable
from typing import cast

import hypothesis
from hypothesis.strategies import text

from named_dataframes import NamedDataFrame
from named_dataframes import NamedSeries


given = cast(Callable[..., Callable[[Callable[..., None]], Callable[..., None]]], hypothesis.given)


@given(contents=text())
def test_series_to_series(contents: str) -> None:
    series = NamedSeries(0, index=[0, 1, 2], name="name", contents=contents)
    assert isinstance(series, NamedSeries)
    assert series.contents == contents
    new = series + 1
    assert isinstance(new, NamedSeries)
    assert new.contents == contents


@given(contents=text())
def test_series_to_dataframe(contents: str) -> None:
    series = NamedSeries(0, index=[0, 1, 2], name="name", contents=contents)
    assert isinstance(series, NamedSeries)
    assert series.contents == contents
    df = series.to_frame()
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents


@given(contents=text())
def test_dataframe_to_dataframe(contents: str) -> None:
    df = NamedDataFrame(0, index=[0, 1, 2], columns=["a", "b", "c"], contents=contents)
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents
    new = df + 1
    assert isinstance(new, NamedDataFrame)
    assert new.contents == contents


@given(contents=text())
def test_dataframe_to_series(contents: str) -> None:
    df = NamedDataFrame(0, index=[0, 1, 2], columns=["a", "b", "c"], contents=contents)
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents
    series = df.a
    assert isinstance(series, NamedSeries)
    assert series.contents == contents

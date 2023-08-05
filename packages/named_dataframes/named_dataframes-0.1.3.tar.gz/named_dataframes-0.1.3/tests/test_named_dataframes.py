from typing import Callable
from typing import cast
from typing import Optional

import hypothesis
from hypothesis.strategies import none
from hypothesis.strategies import text

from named_dataframes import NamedDataFrame
from named_dataframes import NamedSeries


given = cast(Callable[..., Callable[[Callable[..., None]], Callable[..., None]]], hypothesis.given)


@given(contents=none() | text())
def test_series_to_series(contents: Optional[str]) -> None:
    series = NamedSeries(0, index=[0, 1, 2], name="name", contents=contents)
    assert isinstance(series, NamedSeries)
    assert series.contents == contents
    new = series + 1
    assert isinstance(new, NamedSeries)
    assert new.contents == contents


@given(contents=none() | text())
def test_series_to_dataframe(contents: Optional[str]) -> None:
    series = NamedSeries(0, index=[0, 1, 2], name="name", contents=contents)
    assert isinstance(series, NamedSeries)
    assert series.contents == contents
    df = series.to_frame()
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents


@given(contents=none() | text())
def test_dataframe_to_dataframe(contents: Optional[str]) -> None:
    df = NamedDataFrame(0, index=[0, 1, 2], columns=["a", "b", "c"], contents=contents)
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents
    new = df + 1
    assert isinstance(new, NamedDataFrame)
    assert new.contents == contents


@given(contents=none() | text())
def test_dataframe_to_series(contents: Optional[str]) -> None:
    df = NamedDataFrame(0, index=[0, 1, 2], columns=["a", "b", "c"], contents=contents)
    assert isinstance(df, NamedDataFrame)
    assert df.contents == contents
    series = df.a
    assert isinstance(series, NamedSeries)
    assert series.contents == contents


@given(contents1=none() | text(), contents2=none() | text())
def test_series_rename_contents(contents1: Optional[str], contents2: Optional[str]) -> None:
    assert (
        NamedSeries(0, index=[0, 1, 2], name="name", contents=contents1)
        .rename_contents(contents2)
        .contents
        == contents2
    )


@given(contents1=none() | text(), contents2=none() | text())
def test_dataframe_rename_contents(contents1: Optional[str], contents2: Optional[str]) -> None:
    assert (
        NamedDataFrame(0, index=[0, 1, 2], columns=["a", "b", "c"], contents=contents1)
        .rename_contents(contents2)
        .contents
        == contents2
    )

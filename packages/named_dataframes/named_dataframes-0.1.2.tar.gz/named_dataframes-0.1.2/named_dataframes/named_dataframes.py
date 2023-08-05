from __future__ import annotations

from functools import partial
from functools import wraps
from typing import Any
from typing import Callable
from typing import Hashable
from typing import Optional
from typing import Union

from pandas import DataFrame
from pandas import Series


class NamedSeries(Series):
    """A subclass of Series which propagates its name to the DataFrame."""

    def __init__(
        self: NamedSeries, *args: Any, contents: Optional[Hashable] = None, **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.contents = contents

    _metadata = ["contents"]  # dead: disable

    @property
    def _constructor(self: NamedSeries) -> Callable[..., NamedSeries]:  # dead: disable
        return partial(_to_series, self)

    @property
    def _constructor_expanddim(self: NamedSeries) -> Callable[..., NamedDataFrame]:  # dead: disable
        return partial(_to_df, self)


class NamedDataFrame(DataFrame):
    """A subclass of DataFrame which is hashable."""

    def __init__(
        self: NamedDataFrame, *args: Any, contents: Optional[Hashable] = None, **kwargs: Any,
    ) -> None:
        super().__init__(*args, **kwargs)
        self.contents = contents

    _metadata = ["contents"]  # dead: disable

    @property
    def _constructor(self: NamedDataFrame) -> Callable[..., NamedDataFrame]:  # dead: disable
        return partial(_to_df, self)

    @property
    def _constructor_sliced(self: NamedDataFrame) -> Callable[..., NamedSeries]:  # dead: disable
        return partial(_to_series, self)


@wraps(NamedDataFrame)
def _to_df(self: Union[NamedSeries, NamedDataFrame], *args: Any, **kwargs: Any) -> NamedDataFrame:
    return NamedDataFrame(*args, contents=self.contents, **kwargs)


@wraps(NamedSeries)
def _to_series(self: Union[NamedSeries, NamedDataFrame], *args: Any, **kwargs: Any) -> NamedSeries:
    return NamedSeries(*args, contents=self.contents, **kwargs)

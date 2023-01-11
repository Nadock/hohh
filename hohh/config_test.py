# pylint: disable=protected-access, missing-docstring, missing-module-docstring
import datetime as dt

import pytest

from . import config


@pytest.mark.parametrize(
    "now,start,end",
    [
        (dt.datetime(2022, 11, 30), 2020, 2021),
        (dt.datetime(2022, 12, 1), 2021, 2022),
        (dt.datetime(2023, 1, 10), 2021, 2022),
    ],
)
def test_start_end_date(now: dt.datetime, start: int, end: int):
    actual_start, actual_end = config._start_end_dates(now)
    assert start == actual_start.year
    assert end == actual_end.year

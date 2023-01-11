from __future__ import annotations

import dataclasses
import datetime
import os

import pytz

SYDNEY_TZ = pytz.timezone("Australia/Sydney")


@dataclasses.dataclass
class Config:
    """Config for running the hohh CLI."""

    api_key: str = ""
    api_secret: str = ""
    username: str = ""

    hh_start: datetime.datetime = SYDNEY_TZ.localize(
        datetime.datetime(2021, 12, 1, 0, 0, 0, 0), is_dst=None
    )
    hh_end: datetime.datetime = SYDNEY_TZ.localize(
        datetime.datetime(2022, 12, 1, 0, 0, 0, 0), is_dst=None
    )

    def __post_init__(self):
        self.api_key = self.api_key or os.environ.get("LASTFM_KEY", "")
        self.api_secret = self.api_secret or os.environ.get("LASTFM_SECRET", "")

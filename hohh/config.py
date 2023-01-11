from __future__ import annotations

import dataclasses
import datetime
import os

import pytz

SYDNEY_TZ = pytz.timezone("Australia/Sydney")


@dataclasses.dataclass
class Config:  # pylint: disable=too-many-instance-attributes
    """Config for running the hohh CLI."""

    no_spotify: bool

    lastfm_key: str = ""
    lastfm_secret: str = ""
    lastfm_username: str = ""

    spotify_id: str = ""
    spotify_secret: str = ""

    hh_start: datetime.datetime = SYDNEY_TZ.localize(
        datetime.datetime(2021, 12, 1, 0, 0, 0, 0), is_dst=None
    )
    hh_end: datetime.datetime = SYDNEY_TZ.localize(
        datetime.datetime(2022, 12, 1, 0, 0, 0, 0), is_dst=None
    )

    def __post_init__(self):
        self.lastfm_key = self.lastfm_key or os.environ.get("LASTFM_KEY", "")
        self.lastfm_secret = self.lastfm_secret or os.environ.get("LASTFM_SECRET", "")

        self.spotify_id = self.spotify_id or os.environ.get("SPOTIFY_ID", "")
        self.spotify_secret = self.spotify_secret or os.environ.get(
            "SPOTIFY_SECRET", ""
        )

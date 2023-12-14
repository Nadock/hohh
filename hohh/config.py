from __future__ import annotations

import dataclasses
import datetime as dt
import os

import pytz

SYDNEY_TZ = pytz.timezone("Australia/Sydney")


def _start_end_dates(now: dt.datetime) -> tuple[dt.datetime, dt.datetime]:
    # If it is December 1st or later, read results for this year otherwise last year.
    target_year = now.year if now.month == 12 else now.year - 1
    return (
        dt.datetime(target_year - 1, 12, 1, tzinfo=SYDNEY_TZ),
        dt.datetime(target_year, 12, 1, tzinfo=SYDNEY_TZ),
    )


@dataclasses.dataclass
class Config:
    """Config for running the `hohh` CLI."""

    lastfm_key: str = ""
    lastfm_secret: str = ""
    lastfm_username: str = ""

    spotify_id: str = ""
    spotify_secret: str = ""
    no_spotify: bool = False

    start_date: dt.datetime = None  # type: ignore[assignment]
    end_date: dt.datetime = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        self.lastfm_key = self.lastfm_key or os.environ.get("LASTFM_KEY", "")
        self.lastfm_secret = self.lastfm_secret or os.environ.get("LASTFM_SECRET", "")

        self.spotify_id = self.spotify_id or os.environ.get("SPOTIFY_ID", "")
        self.spotify_secret = self.spotify_secret or os.environ.get(
            "SPOTIFY_SECRET",
            "",
        )

        self.start_date = _start_end_dates(dt.datetime.now(SYDNEY_TZ))[0]
        self.end_date = _start_end_dates(dt.datetime.now(SYDNEY_TZ))[1]

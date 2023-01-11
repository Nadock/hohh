from __future__ import annotations

import dataclasses
import datetime
from typing import Generator

import pylast  # type: ignore

from . import config


@dataclasses.dataclass
class Track:
    """A track/song read from Last.fm."""

    # TODO: Move this into a separate models module, it's not specific to Last.fm

    title: str
    artist: str
    date: datetime.datetime | None = None

    @classmethod
    def from_pylast(cls, track: pylast.Track) -> Track:
        """Create a `Track` from a `pylast.Track` with no network requests."""
        return cls(title=track.title, artist=track.artist.name)


def get_playback_history(cfg: config.Config) -> Generator[Track, None, None]:
    """
    Return the user's Last.fm playback history for the eligible dates.

    Playback history is returned as a generator of `Track` objects. These tracks have
    not been filtered for eligibility beyond the fact they were listened to during the
    eligibility window.
    """
    return _render_tracks(_dedupe_tracks(_get_unfiltered_tracks(cfg)))


def _get_unfiltered_tracks(
    cfg: config.Config,
) -> Generator[pylast.Track, None, None]:
    """Retrieve tracks played during the eligible window from Last.fm."""
    network = pylast.LastFMNetwork(
        api_key=cfg.lastfm_key,
        api_secret=cfg.lastfm_secret,
        username=cfg.lastfm_username,
    )

    tracks = network.get_authenticated_user().get_recent_tracks(
        time_from=cfg.start_date,
        time_to=cfg.end_date,
        stream=True,
        now_playing=False,
        limit=None,
    )

    for track in tracks:
        yield track.track


def _dedupe_tracks(
    tracks: Generator[pylast.Track, None, None]
) -> Generator[pylast.Track, None, None]:
    """Remove duplicate Tracks from the generator."""
    cache = set()
    for track in tracks:
        key = hash(track.get_url())
        if key not in cache:
            cache.add(key)
            yield track


def _render_tracks(
    tracks: Generator[pylast.Track, None, None]
) -> Generator[Track, None, None]:
    """Convert each track from `pylast.Track` type into our `Track` type."""
    for track in tracks:
        yield Track.from_pylast(track)

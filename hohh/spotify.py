import base64
import datetime
from typing import Generator

import requests

from . import config, lastfm


class SpotifyClient:
    """Simple API client for interacting with the Spotify API."""

    def __init__(self, spotify_id: str, spotify_secret: str):
        self._id = spotify_id
        self._secret = spotify_secret
        self._token: str = ""
        self._expires_at: datetime.datetime = datetime.datetime.now()
        self._base_url = "https://api.spotify.com/v1"

        if not self._id or not self._secret:
            raise ValueError("spotify_id and spotify_secret must both be set")

    def _auth(self):
        if datetime.datetime.now() <= self._expires_at:
            return

        basic_auth = base64.b64encode(
            f"{self._id}:{self._secret}".encode("utf-8")
        ).decode("utf-8")

        resp = requests.post(
            "https://accounts.spotify.com/api/token",
            headers={"Authorization": f"Basic {basic_auth}"},
            data={"grant_type": "client_credentials"},
            timeout=10.0,
        )

        resp.raise_for_status()
        _json = resp.json()
        if "access_token" not in _json:
            raise ValueError(f"Invalid response from Spotify: {_json}")
        if "expires_in" not in _json:
            raise ValueError(f"Invalid response from Spotify: {_json}")

        self._token = _json["access_token"]
        self._expires_at = datetime.datetime.now() + datetime.timedelta(
            seconds=_json["expires_in"] - 60
        )

    def search_track(self, track: lastfm.Track) -> dict | None:
        """
        Search Spotify's API for a track, returning the first result found.

        Search API:
        https://developer.spotify.com/documentation/web-api/reference/#/operations/search
        """
        self._auth()

        params = {
            "type": "track",
            "q": f"{track.title} artist:{track.artist}",
        }
        headers = {"Authorization": f"Bearer {self._token}"}

        resp = requests.get(
            self._base_url + "/search", params=params, headers=headers, timeout=10.0
        )
        resp.raise_for_status()

        try:
            return resp.json()["tracks"]["items"][0]
        except Exception:  # pylint: disable=broad-except
            return None


def filter_tracks(
    cfg: config.Config,
    client: SpotifyClient,
    tracks: Generator[lastfm.Track, None, None],
) -> Generator[lastfm.Track, None, None]:
    """
    Filter `Track`s in generator to include only tracks released during the
    eligibility window.
    """
    for track in tracks:
        search_result = client.search_track(track)
        if not search_result:
            yield track
            continue

        match search_result["album"]["release_date_precision"]:
            case "year":
                time_format = "%Y"
            case "month":
                time_format = "%Y-%m"
            case "day":
                time_format = "%Y-%m-%d"
            case _:
                raise ValueError(
                    "Unknown release_date_precision="
                    + search_result["album"]["release_date_precision"]
                )

        date = config.SYDNEY_TZ.localize(
            datetime.datetime.strptime(
                search_result["album"]["release_date"], time_format
            ),
            is_dst=None,
        )
        track.date = date

        if cfg.start_date <= date <= cfg.end_date:
            yield track

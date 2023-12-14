import argparse
import csv
import sys

from hohh import spotify

from . import config, lastfm


def main() -> None:  # noqa: D103
    args = setup_argparse().parse_args()
    cfg = config.Config(lastfm_username=args.username, no_spotify=args.no_spotify)

    tracks = lastfm.get_playback_history(cfg)

    if not cfg.no_spotify:
        client = spotify.SpotifyClient(
            spotify_id=cfg.spotify_id,
            spotify_secret=cfg.spotify_secret,
        )
        tracks = spotify.filter_tracks(cfg, client, tracks)

    print(
        f'Getting tracks for LastFM user "{cfg.lastfm_username}"'
        + (" without Spotify" if cfg.no_spotify else " with filtering via Spotify")
        + "...",
        file=sys.stderr,
        flush=True,
    )

    writer = csv.DictWriter(
        sys.stdout,
        fieldnames=["Title", "Artist", "Date"],
        quoting=csv.QUOTE_ALL,
    )
    writer.writeheader()

    for track in tracks:
        writer.writerow(
            {"Title": track.title, "Artist": track.artist, "Date": track.date},
        )
        sys.stdout.flush()


def setup_argparse() -> argparse.ArgumentParser:
    """Create an `argparse.ArgumentParser` to parse `hohh` CLI args."""
    parser = argparse.ArgumentParser(
        prog="hohh",
        description=(
            "Generate a list of tracks that you've heard that are eligible for this "
            "year's Triple J's Hottest 100."
        ),
    )

    parser.add_argument(
        "-s",
        "--no-spotify",
        action="store_true",
        help="Don't filter playback history with release date data from Spotify",
    )

    parser.add_argument(
        "username",
        metavar="USER",
        type=str,
        help="Your Last.fm username, to retrieve playback history.",
    )

    return parser

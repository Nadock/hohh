import argparse

from hohh import spotify

from . import config, lastfm


def main():
    # pylint: disable=missing-docstring, invalid-name
    args = setup_argparse().parse_args()
    cfg = config.Config(lastfm_username=args.username, no_spotify=args.no_spotify)

    tracks = lastfm.get_playback_history(cfg)

    if not cfg.no_spotify:
        client = spotify.SpotifyClient(
            spotify_id=cfg.spotify_id, spotify_secret=cfg.spotify_secret
        )
        tracks = spotify.filter_tracks(cfg, client, tracks)

    print("Title, Artist, Date")
    for t in tracks:
        date = t.date or ""
        print(f'"{t.title}", "{t.artist}", "{date}"')


def setup_argparse() -> argparse.ArgumentParser:
    """Create an `argparse.ArgumentParser` to parse `hohh` CLI args."""
    parser = argparse.ArgumentParser(
        prog="hohh",
        description=(
            "Generate a list of tracks that you've heard that are eligible for this "
            + "year's Triple J's Hottest 100."
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

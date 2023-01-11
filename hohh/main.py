import argparse

from . import config, lastfm


def main():  # pylint: disable=missing-docstring
    args = setup_argparse().parse_args()
    cfg = config.Config(username=args.username)

    for track in lastfm.get_playback_history(cfg):
        print(f"{track=}")


def setup_argparse() -> argparse.ArgumentParser:
    """Create an `argparse.ArgumentParser` to parse `hohh` CLI args."""
    # TODO: Set app name correctly
    parser = argparse.ArgumentParser()

    # TODO: Help/description strings
    parser.add_argument("username", metavar="USER", type=str)

    return parser

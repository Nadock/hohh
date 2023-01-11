# Hottest One-Hundred Helper

Do you like to vote in the Australian music competition "[Triple J's Hottest One-Hundred](https://www.abc.net.au/triplej/hottest100)" but you don't remember what songs you've listened to that came out last year? Well, assuming you have a Last.fm account, this tool can help you generate a list of all the eligible songs you've listened to in the last year.

## Setup

1. Clone or download the repo — `hohh` is not published to PyPI yet.
2. `cp example.env .env`
3. Setup a Last.fm API Account.

Follow the steps [here](https://www.last.fm/api/account/create) to create one, then put your **API Key** and **Shared Secret** in your `.env` file.

4. Setup a Spotify API App

This is only needed to retrieve release dates for tracks, as Last.fm has shitty
data. This step is optional if you also supply the `-s/--no-spotify` CLI flag.

If you don't already have a Spotify account make one first, then go [here](https://developer.spotify.com/dashboard/applications) to create an API app. Once you have done that, put your **Client ID** and **Client Secret** in your `.env` file.

5. Install dependencies via Poetry.

This CLI is a Python package and it has a few important dependencies. Ensure you have
[Poetry](https://python-poetry.org) installed, then run `poetry install` to setup a
local virtual environment.

## Usage

Once you've done the [setup](Setup) steps above once, you can run the CLI for any
Last.fm user who has public listen history and your own account. Use the provided
`Taskfile` to run the CLI or export your `.env` variables into your shell and then run
the CLI.

```console
task hohh -- nadock

Title, Artist, Date
"Sideways", "Carly Rae Jepsen", "2022-10-21 00:00:00+11:00"
"Joshua Tree", "Carly Rae Jepsen", "2022-10-21 00:00:00+11:00"
```

The only argument to CLI is the username of the Last.fm user you want to retrieve
stats for.

The results are printed in CSV format so you can redirect the results into a file
like `task hohh -- $user > results.csv`.

## A Note on Accuracy

Because we have to try and pair tracks from two distinct systems (ie: Last.fm and
Spotify), the resulting list may have `Date` values that are empty if no result could
be found in Spotify. Additionally, if the Spotify search returned the "wrong" track
then that track's release date will be used and will be different to the actual release
date.

If you want to just get all your listen history without filter via Spotify, use
the `-s/--no-spotify` CLI flag.

## MVP Warning

This was built pretty much all in one day, and in it's current state it almost certainly
has ugly bugs and confusing errors. If you find any of them please open an PR or issue.

Also, for the same reasons this package is not currently published to PyPI. The only way
to use it is to clone the repo and run it locally yourself.

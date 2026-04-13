# anitrack

anitrack is a command line tool that lets you fetch anime data
from public APIs like [MyAnimeList](https://myanimelist.net/) (via Jikan) and [Anilist](https://anilist.co/).

You can search anime by title or ID and export the data to a CSV file.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Result Examples](#result-examples)
- [Running Tests](#running-tests)

---

## Features

### Search by Title or ID

Retrieve anime data from the API using either a title string or a numeric ID. Each result includes:

- `id` — unique anime identifier
- `english_title` / `romaji_title` — localized title variants
- `average_score` — community rating
- `episodes` — total episode count
- `genres` — list of genre tags

### Export Anime Data

Save fetched anime data to a CSV file.

---

## Project Structure

```bash
anitrack/
├── main.py                                 # Entry point; argparser and subcommands
├── core/
│   ├── models/
│   │    ├── anime_model.py                 # Dataclasses: AnimeDataModel
│   │    └── protocols.py                   # Protocols: FetchersProtocol
│   ├── cli/
│   │    ├── fetch_cli.py                   # Fetch data then print
│   │    ├── export_cli.py                  # Fetch data then save
│   │    └── cli_utils.py                   # CLI Helper functions
│   ├── fetchers/
│   │    ├── base_fetcher.py                # Abstract base class for fetchers
│   │    ├── fetcher_factory.py             # Fetchers factory
│   │    ├── anilist_fetcher.py             # Fetcher for anilist API
│   │    └── jikan_fetcher.py               # Fetcher for jikan API
│   ├── exceptions.py                       # Custom exception hierarchy
│   ├── normalizer.py                       # API Data normalizer
│   └── file_handler.py                     # File handler for DataIO
├── storage/
│   └── *.csv                               # Saved data outputs
├── tests/
│   ├── fetchers_mock_data.py               # Fetcher mock classes: MockAnilistFetcher, MockJikanFetcher
│   ├── test_fetcher_anilist.py
│   ├── test_fetcher_jikan.py
│   └── test_normalizer.py
└── requirements.txt                        # Dependencies: requests, jikanpy-v4, pandas
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rifki-NQ/anitrack

# 2. Navigate into the project directory
cd anitrack

# 3. Install dependencies
pip install -r requirements.txt
```

---

## Usage

``` bash
<command> [options]
```

### Commands

#### `fetch` — Fetch anime data

```bash
fetch --source <source> (--title <title> | --id <id>) [--entry <entry> | --show-title [--max-entry <max-entry>]]
```

**Options:**

| Flag | Type | Required | Description |
| ---- | ---- | -------- | ----------- |
| `--source` | string | ✅ Yes | Data source to fetch from. Choices: `anilist`, `jikan`, `all` |
| `--title` | string | ✅ One of | Search anime by title |
| `--id` | int | ✅ One of | Fetch anime by ID |
| `--entry` | int | ❌ No | Entry number for search result (default: `none`) |
| `--show-title` | flag | ❌ No | display the matched entry's title (default: `false`) |
| `--max-entry` | int | ❌ No | Max anime titles to display (default: `none`) |

> - `--title` and `--id` are mutually exclusive — you must provide exactly one.
> - `--entry` and `--show-title` are only valid when `--title` is used.
> - `--entry` and `--show-title` are mutually exclusive — provide at most one.
> - `--max-entry` only works with `--show-title`.

**Examples:**

```bash
# Fetch by title
python main.py fetch --source anilist --title "Steins;Gate"

# Fetch by ID
python main.py fetch --source jikan --id 9253

# Show fetch subcommand help
python main.py fetch --help
```

#### `export` — Fetch and save anime data to a file

```bash
export --source <source> (--title <title> | --id <id>) --path <path> [--entry <entry> | --save-all [--max-entry <max-entry>]] [--overwrite]
```

**Options:**

| Flag | Type | Required | Description |
| ---- | ---- | -------- | ----------- |
| `--source` | string | ✅ Yes | Data source to fetch from. Choices: `anilist`, `jikan`, `all` |
| `--title` | string | ✅ One of | Search anime by title |
| `--id` | int | ✅ One of | Fetch anime by ID |
| `--path` | string | ✅ Yes | Destination file path to save the exported data |
| `--entry` | int | ❌ No | Entry number for search result (default: `none`) |
| `--save-all` | flag | ❌ No | Save all entries from search result (default: `false`) |
| `--max-entry` | int | ❌ No | Max anime entries to save (default: `none`) |
| `--overwrite` | flag | ❌ No | Overwrite the data if it's not empty (default: `false`) |

> - `--path` must be inside the `storage/` folder.
> - `--title` and `--id` are mutually exclusive — you must provide exactly one.
> - `--entry`and `--save-all` are only valid when `--title` is used.
> - `--entry`and `--save-all` are mutually exclusive — provide at most one.
> - `--max-entry` only works with `--save-all`.

**Examples:**

```bash
# Export by title
python main.py export --source anilist --title "Steins;Gate" --path storage/data.csv

# Export by ID
python main.py export --source jikan --id 9253 --path storage/data.csv

# Export and overwrite the data
python main.py export --source all --title "Steins;Gate" --path storage/data.csv --overwrite

# Show export subcommand help
python main.py export --help
```

---

## Result Examples

**Command:**

```bash
python main.py fetch --source jikan --title "one piece" --entry 1
```

**Result:**

```bash
source: jikan
id: 21
english_title: One Piece
romaji_title: One Piece
average_score: 8.73
episodes: None
genres: ['Action', 'Adventure', 'Fantasy']
```

---

**Command:**

```bash
python main.py fetch --source all --title "mushoku tensei"
```

**Result:**

```bash
source: anilist | jikan
id: 108465 | 39535
english_title: Mushoku Tensei: Jobless Reincarnation | Mushoku Tensei: Jobless Reincarnation
romaji_title: Mushoku Tensei: Isekai Ittara Honki Dasu | Mushoku Tensei: Isekai Ittara Honki Dasu
average_score: 82 | 8.33
episodes: 11 | 11
genres: ['Adventure', 'Drama', 'Ecchi', 'Fantasy'] | ['Adventure', 'Drama', 'Fantasy', 'Ecchi']
```

---

**Command:**

```bash
python main.py export --source anilist --title "steins gate" --path storage/data.csv --overwrite
```

**Result:**

```bash
source,id,english_title,romaji_title,average_score,episodes,genres
anilist,9253,Steins;Gate,Steins;Gate,89,24,"['Drama', 'Psychological', 'Sci-Fi', 'Thriller']"
```

> The exported data is saved to `storage/data.csv`.

---

**Command:**

```bash
python main.py export --source anilist --title "steins gate" --path storage/data.csv --entry 1
```

**Result:**

```bash
source,id,english_title,romaji_title,average_score,episodes,genres
anilist,9253,Steins;Gate,Steins;Gate,89,24,"['Drama', 'Psychological', 'Sci-Fi', 'Thriller']"
anilist,21127,Steins;Gate 0,Steins;Gate 0,84,23,"['Drama', 'Psychological', 'Sci-Fi', 'Thriller']"
```

> - The exported data is saved to `storage/data.csv`.
> - If the `--overwrite` flag is not provided, new data will be appended to the       existing file instead of overwriting it.

---

## Running Tests

```bash
pytest tests/
```

The test suite covers:

- `test_fetcher_anilist.py` - verifies that the `FetchAnilist` return expected data values and type from the `API`
- `test_fetcher_jikan.py` - verifies that the `FetchJikan` return expected data values and type from the `API`
- `test_normalizer.py` - verifies the normalization flow using mocked fetcher data

---

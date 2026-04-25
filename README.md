# joho

joho is a command line tool that lets you fetch anime data
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

``` bash
joho/
├── joho/
│   ├── __init__.py
│   ├── main.py                            # Entry point; argparser and subcommands
│   └── core/
│       ├── __init__.py
│       ├── constants.py                   # Shared constants
│       ├── exceptions.py                  # Custom exception hierarchy
│       ├── file_handler.py                # File handler for DataIO
│       ├── models/
│       │   ├── anime_model.py             # Dataclasses: AnimeDataModel
│       │   └── protocols.py               # Protocols: FetchersProtocol, NormalizerProtocol
│       ├── cli/
│       │   ├── fetch_cli.py               # Fetch data then print
│       │   ├── export_cli.py              # Fetch data then save
│       │   └── cli_utils.py               # CLI Helper functions
│       ├── fetchers/
│       │   ├── base_fetcher.py            # Abstract base class for fetchers
│       │   ├── fetcher_factory.py         # Fetchers factory
│       │   ├── anilist_fetcher.py         # Fetcher for AniList API
│       │   └── jikan_fetcher.py           # Fetcher for Jikan API
│       └── normalizers/
│           ├── base_normalizer.py         # Abstract base class for normalizers
│           ├── normalizer_factory.py      # Normalizers factory
│           ├── anilist_normalizer.py      # Normalizer for AniList API data
│           └── jikan_normalizer.py        # Normalizer for Jikan API data
├── tests/
│   ├── fetchers_mock_data.py              # Mock classes: MockAnilistFetcher, MockJikanFetcher
│   ├── test_fetcher_anilist.py
│   ├── test_fetcher_jikan.py
│   └── test_normalizer.py
├── storage/
│   └── *.csv                              # Saved data outputs
├── pyproject.toml                         # Project metadata and dependencies
├── README.md
└── .gitignore
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rifki-NQ/joho

# 2. Navigate into the project directory
cd joho

# 3. Create a virtual environment

# Linux / macOS
python3 -m venv .venv

# Windows
python -m venv .venv

# 4. Activate the virtual environment

# Linux / macOS
source .venv/bin/activate

# Windows
.venv\Scripts\activate

# 5. Install dependencies
pip install -e .

# (Optional) Install dev dependencies
pip install -e ".[dev]"
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

# Fetch anime titles
python main.py fetch --source all --title "mushoku tensei" --show-title

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

# Export all entries
python main.py export --source anilist --title "mushoku tensei" --path storage/data.csv --save-all

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
source: anilist
id: 108465
english_title: Mushoku Tensei: Jobless Reincarnation
romaji_title: Mushoku Tensei: Isekai Ittara Honki Dasu
average_score: 82
episodes: 11
genres: ['Adventure', 'Drama', 'Ecchi', 'Fantasy']

source: jikan
id: 39535
english_title: Mushoku Tensei: Jobless Reincarnation
romaji_title: Mushoku Tensei: Isekai Ittara Honki Dasu
average_score: 8.33
episodes: 11
genres: ['Adventure', 'Drama', 'Fantasy', 'Ecchi']
```

---

**Command:**

```bash
python main.py fetch --source jikan --title "mushoku tensei" --show-title --max-entry 10
```

**Result:**

```bash
Source: jikan
Romaji title | English title
0. Mushoku Tensei: Isekai Ittara Honki Dasu | Mushoku Tensei: Jobless Reincarnation
1. Mushoku Tensei II: Isekai Ittara Honki Dasu | Mushoku Tensei: Jobless Reincarnation Season 2
2. Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2 | Mushoku Tensei: Jobless Reincarnation Season 2 Part 2
3. Mushoku Tensei II: Isekai Ittara Honki Dasu - Shugo Jutsushi Fitz | Mushoku Tensei: Jobless Reincarnation Season 2 - Episode 0 "Guardian Fitz"
4. Mushoku Tensei: Isekai Ittara Honki Dasu - Eris no Goblin Toubatsu | Mushoku Tensei: Jobless Reincarnation - Eris the Goblin Slayer
5. Mushoku Tensei: Isekai Ittara Honki Dasu Part 2 | Mushoku Tensei: Jobless Reincarnation Part 2
6. Mushoku Tensei III: Isekai Ittara Honki Dasu | Mushoku Tensei: Jobless Reincarnation Season 3
7. Google Play de Chou Musou!? Tensei shitara Android User Datta. Special | None
8. Google Play de Chou Musou!? Tensei shitara Android User Datta. | None
9. Rakudai Kenja no Gakuin Musou: Nidome no Tensei, S-Rank Cheat Majutsushi Boukenroku | The Failed Sage's Academy Domination
```

---

**Command:**

```bash
python main.py export --source anilist --title "steins gate" --path storage/data.csv
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
anilist,9253,Steins;Gate,Steins;Gate,89,24,"['Drama', 'Psychological', 'Sci-Fi', 'Thriller']" # <- previous data
anilist,21127,Steins;Gate 0,Steins;Gate 0,84,23,"['Drama', 'Psychological', 'Sci-Fi', 'Thriller']" # <- appends new data
```

> - The exported data is saved to `storage/data.csv`.
> - If the `--overwrite` flag is not provided, new data will be appended to the existing file instead of overwriting it.

---

**Command:**

```bash
python main.py export --source all --title "mushoku tensei" --path storage/data.csv --save-all --max-entry 5 --overwrite
```

**Result:**

```bash
source,id,english_title,romaji_title,average_score,episodes,genres
anilist,108465,Mushoku Tensei: Jobless Reincarnation,Mushoku Tensei: Isekai Ittara Honki Dasu,82.0,11.0,"['Adventure', 'Drama', 'Ecchi', 'Fantasy']"
anilist,146065,Mushoku Tensei: Jobless Reincarnation Season 2,Mushoku Tensei II: Isekai Ittara Honki Dasu,81.0,13.0,"['Adventure', 'Drama', 'Ecchi', 'Fantasy']"
anilist,178789,Mushoku Tensei: Jobless Reincarnation Season 3,Mushoku Tensei III: Isekai Ittara Honki Dasu,,,"['Adventure', 'Drama', 'Ecchi', 'Fantasy']"
anilist,166873,Mushoku Tensei: Jobless Reincarnation Season 2 Part 2,Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2,83.0,12.0,"['Adventure', 'Drama', 'Ecchi', 'Fantasy']"
anilist,127720,Mushoku Tensei: Jobless Reincarnation Cour 2,Mushoku Tensei: Isekai Ittara Honki Dasu Part 2,85.0,12.0,"['Adventure', 'Drama', 'Ecchi', 'Fantasy']"
jikan,39535,Mushoku Tensei: Jobless Reincarnation,Mushoku Tensei: Isekai Ittara Honki Dasu,8.33,11.0,"['Adventure', 'Drama', 'Fantasy', 'Ecchi']"
jikan,51179,Mushoku Tensei: Jobless Reincarnation Season 2,Mushoku Tensei II: Isekai Ittara Honki Dasu,8.2,12.0,"['Adventure', 'Drama', 'Fantasy', 'Ecchi']"
jikan,55888,Mushoku Tensei: Jobless Reincarnation Season 2 Part 2,Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2,8.39,12.0,"['Adventure', 'Drama', 'Fantasy', 'Ecchi']"
jikan,55818,"Mushoku Tensei: Jobless Reincarnation Season 2 - Episode 0 ""Guardian Fitz""",Mushoku Tensei II: Isekai Ittara Honki Dasu - Shugo Jutsushi Fitz,7.54,1.0,"['Adventure', 'Drama', 'Fantasy', 'Ecchi']"
jikan,50360,Mushoku Tensei: Jobless Reincarnation - Eris the Goblin Slayer,Mushoku Tensei: Isekai Ittara Honki Dasu - Eris no Goblin Toubatsu,7.79,1.0,"['Adventure', 'Drama', 'Fantasy']"
```

> - The exported data is saved to `storage/data.csv`.
> - `--max-entry` limits the number of entries saved per source to the specified value.
> - With the `--overwrite` flag, all previous data gets overwritten with the new data.

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

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

- `data_source`
- `romaji_title`
- `english_title`
- `format`
- `episodes`
- `status`
- `average_score`
- `duration`
- `start_date`
- `end_date`
- `studio`
- `source`
- `genres`
- `all_time_rank`
- `all_time_popularity`

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
│       │   ├── __init__.py
│       │   ├── anime_model.py             # Dataclasses: AnimeDataModel
│       │   └── protocols.py               # Protocols: FetchersProtocol, NormalizerProtocol
│       ├── cli/
│       │   ├── __init__.py
│       │   ├── fetch_cli.py               # Fetch data then print
│       │   ├── export_cli.py              # Fetch data then save
│       │   └── cli_utils.py               # CLI Helper functions
│       ├── fetchers/
│       │   ├── __init__.py
│       │   ├── base_fetcher.py            # Abstract base class for fetchers
│       │   ├── fetcher_factory.py         # Fetchers factory
│       │   ├── anilist_fetcher.py         # Fetcher for AniList API
│       │   └── jikan_fetcher.py           # Fetcher for Jikan API
│       └── normalizers/
│           ├── __init__.py
│           ├── base_normalizer.py         # Abstract base class for normalizers
│           ├── normalizer_factory.py      # Normalizers factory
│           ├── anilist_normalizer.py      # Normalizer for AniList API data
│           └── jikan_normalizer.py        # Normalizer for Jikan API data
├── tests/
│   ├── __init__.py
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
joho <command> [options]
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
joho fetch --source anilist --title "Steins;Gate"

# Fetch by ID
joho fetch --source jikan --id 9253

# Fetch anime titles
joho fetch --source all --title "mushoku tensei" --show-title

# Show fetch subcommand help
joho fetch --help
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
joho export --source anilist --title "Steins;Gate" --path storage/data.csv

# Export by ID
joho export --source jikan --id 9253 --path storage/data.csv

# Export and overwrite the data
joho export --source all --title "Steins;Gate" --path storage/data.csv --overwrite

# Export all entries
joho export --source anilist --title "mushoku tensei" --path storage/data.csv --save-all

# Show export subcommand help
joho export --help
```

---

## Result Examples

**Command:**

```bash
joho fetch --source jikan --title "one piece" --entry 1
```

**Result:**

```bash
data_source: jikan
id: 21
romaji_title: One Piece
english_title: One Piece
format: TV
episodes: None
status: Currently Airing
average_score: 8.73
duration: 00:24
start_date: 1999-10-20
end_date: None
studio: Toei Animation
source: Manga
genres: Action|Adventure|Fantasy
all_time_rank: 54
all_time_popularity: 17
```

---

**Command:**

```bash
joho fetch --source all --title "mushoku tensei"
```

**Result:**

```bash
data_source: anilist
id: 108465
romaji_title: Mushoku Tensei: Isekai Ittara Honki Dasu
english_title: Mushoku Tensei: Jobless Reincarnation
format: TV
episodes: 11
status: FINISHED
average_score: 82
duration: 00:24
start_date: 2021-01-11
end_date: 2021-03-22
studio: Studio Bind
source: LIGHT_NOVEL
genres: Adventure|Drama|Ecchi|Fantasy
all_time_rank: 190
all_time_popularity: 66

data_source: jikan
id: 39535
romaji_title: Mushoku Tensei: Isekai Ittara Honki Dasu
english_title: Mushoku Tensei: Jobless Reincarnation
format: TV
episodes: 11
status: Finished Airing
average_score: 8.33
duration: 00:23
start_date: 2021-01-11
end_date: 2021-03-22
studio: Studio Bind
source: Light novel
genres: Adventure|Drama|Fantasy|Ecchi
all_time_rank: 293
all_time_popularity: 84

2 / 2 fetched successfully
```

---

**Command:**

```bash
joho fetch --source jikan --title "mushoku tensei" --show-title --max-entry 10
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
joho export --source anilist --title "steins gate" --path storage/data.csv
```

**Result:**

```bash
data_source,id,romaji_title,english_title,format,episodes,status,average_score,duration,start_date,end_date,studio,source,genres,all_time_rank,all_time_popularity
anilist,9253,Steins;Gate,Steins;Gate,TV,24,FINISHED,89,00:24,2011-04-06,2011-09-14,WHITE FOX,VISUAL_NOVEL,Drama|Psychological|Sci-Fi|Thriller,7,27
```

> The exported data is saved to `storage/data.csv`.

---

**Command:**

```bash
joho export --source anilist --title "steins gate" --path storage/data.csv --entry 1
```

**Result:**

```bash
data_source,id,romaji_title,english_title,format,episodes,status,average_score,duration,start_date,end_date,studio,source,genres,all_time_rank,all_time_popularity
anilist,9253,Steins;Gate,Steins;Gate,TV,24,FINISHED,89,00:24,2011-04-06,2011-09-14,WHITE FOX,VISUAL_NOVEL,Drama|Psychological|Sci-Fi|Thriller,7,27
anilist,21127,Steins;Gate 0,Steins;Gate 0,TV,23,FINISHED,84,00:24,2018-04-12,2018-09-27,WHITE FOX,VISUAL_NOVEL,Drama|Psychological|Sci-Fi|Thriller,102,221
```

> - The exported data is saved to `storage/data.csv`.
> - If the `--overwrite` flag is not provided, new data will be appended to the existing file instead of overwriting it.

---

**Command:**

```bash
joho export --source all --title "mushoku tensei" --path storage/data.csv --save-all --max-entry 5 --overwrite
```

**Result:**

```bash
data_source,id,romaji_title,english_title,format,episodes,status,average_score,duration,start_date,end_date,studio,source,genres,all_time_rank,all_time_popularity
anilist,108465,Mushoku Tensei: Isekai Ittara Honki Dasu,Mushoku Tensei: Jobless Reincarnation,TV,11.0,FINISHED,82.0,00:24,2021-01-11,2021-03-22,Studio Bind,LIGHT_NOVEL,Adventure|Drama|Ecchi|Fantasy,190.0,66.0
anilist,146065,Mushoku Tensei II: Isekai Ittara Honki Dasu,Mushoku Tensei: Jobless Reincarnation Season 2,TV,13.0,FINISHED,81.0,00:24,2023-07-03,2023-09-25,Studio Bind,LIGHT_NOVEL,Adventure|Drama|Ecchi|Fantasy,231.0,199.0
anilist,178789,Mushoku Tensei III: Isekai Ittara Honki Dasu,Mushoku Tensei: Jobless Reincarnation Season 3,TV,,NOT_YET_RELEASED,,,2026-07-06,,Studio Bind,LIGHT_NOVEL,Adventure|Drama|Ecchi|Fantasy,,
anilist,166873,Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2,Mushoku Tensei: Jobless Reincarnation Season 2 Part 2,TV,12.0,FINISHED,83.0,00:24,2024-04-08,2024-07-01,Studio Bind,LIGHT_NOVEL,Adventure|Drama|Ecchi|Fantasy,133.0,282.0
anilist,127720,Mushoku Tensei: Isekai Ittara Honki Dasu Part 2,Mushoku Tensei: Jobless Reincarnation Cour 2,TV,12.0,FINISHED,85.0,00:24,2021-10-04,2021-12-20,Studio Bind,LIGHT_NOVEL,Adventure|Drama|Ecchi|Fantasy,73.0,128.0
jikan,39535,Mushoku Tensei: Isekai Ittara Honki Dasu,Mushoku Tensei: Jobless Reincarnation,TV,11.0,Finished Airing,8.33,00:23,2021-01-11,2021-03-22,Studio Bind,Light novel,Adventure|Drama|Fantasy|Ecchi,293.0,84.0
jikan,51179,Mushoku Tensei II: Isekai Ittara Honki Dasu,Mushoku Tensei: Jobless Reincarnation Season 2,TV,12.0,Finished Airing,8.2,00:23,2023-07-10,2023-09-25,Studio Bind,Light novel,Adventure|Drama|Fantasy|Ecchi,448.0,308.0
jikan,55888,Mushoku Tensei II: Isekai Ittara Honki Dasu Part 2,Mushoku Tensei: Jobless Reincarnation Season 2 Part 2,TV,12.0,Finished Airing,8.39,00:23,2024-04-08,2024-07-01,Studio Bind,Light novel,Adventure|Drama|Fantasy|Ecchi,236.0,437.0
jikan,55818,Mushoku Tensei II: Isekai Ittara Honki Dasu - Shugo Jutsushi Fitz,"Mushoku Tensei: Jobless Reincarnation Season 2 - Episode 0 ""Guardian Fitz""",TV Special,1.0,Finished Airing,7.54,00:24,2023-07-03,,Studio Bind,Light novel,Adventure|Drama|Fantasy|Ecchi,2026.0,1144.0
jikan,50360,Mushoku Tensei: Isekai Ittara Honki Dasu - Eris no Goblin Toubatsu,Mushoku Tensei: Jobless Reincarnation - Eris the Goblin Slayer,Special,1.0,Finished Airing,7.79,00:23,2022-03-16,,Studio Bind,Light novel,Adventure|Drama|Fantasy,1193.0,1312.0
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

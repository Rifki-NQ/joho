# anitrack

CLI-based tool used for getting anime data from sources like MAL or Anilist

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Intallation](#installation)
- [Usage](#usage)
- [Running Tests](#running-tests)

---

## Features

### Search by Title or ID

Query anime data from the API using either a title string or a numeric ID. Each result includes:

- `id` — unique anime identifier
- `english_title` / `romaji_title` — localized title variants
- `average_score` — community rating
- `episodes` — total episode count
- `genres` — list of genre tags

---

## Project Structure

```bash
anitrack/
├── main.py                                 # Entry point; argparser and subcommands
├── core/
│   ├── models
│   │    └── anime_model.py                 # Dataclasses: AnimeDataModel
│   ├── cli
│   │    └── fetch_cli.py                   # Query handler for fetch subcommands
│   ├── exceptions.py                       # Custom exception hierarchy
│   ├── fetcher.py                          # API fetcher: FetchAnilist
│   ├── normalizer.py                       # API Data normalizer
│   └── file_handler.py                     # File handler for DataIO
├── storage
│   └── *.csv                               # Saved data outputs
└── requirements.txt                        # Dependencies: requests, jikanpy
```

---

## Installation

```bash
# 1. Clone the repository
git clone https://github.com/Rifki-NQ/RandomDatasetGenerator

# 2. Navigate into the project directory
cd RandomDatasetGenerator

# 3. Install dependencies
pip install -r requirements.txt
```

## Usage

``` bash
<command> [options]
```

### Commands

#### `fetch` — Fetch anime data

```bash
fetch --source <source> (--title <title> | --id <id>)
```

**Options:**

| Flag | Type | Required | Description |
| ---- | ---- | -------- | ----------- |
| `--source` | string | ✅ Yes | Data source to fetch from. Choices: `anilist` |
| `--title` | string | ✅ One of | Search anime by title |
| `--id` | int | ✅ One of | Fetch anime by ID |

> `--title` and `--id` are mutually exclusive — you must provide exactly one.

**Examples:**

```bash
# Fetch by title
python main.py fetch --source anilist --title "Steins;Gate"

# Fetch by ID
python main.py fetch --source anilist --id 9253

# Show fetch subcommand help
python main.py fetch --help
```

---

### General Help

```bash
python main.py --help
python main.py fetch --help
```

---

## Running Tests

```bash
pytest tests/
```

The test suite covers:

- `test_fetcher_anilist.py` - verifies that the `FetchAnilist` return expected data values and type from the `API`

---

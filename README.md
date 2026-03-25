# anitrack
CLI-based tool used for getting anime data from sources like MAL or Anilist

## Table of Contents
- [Project Structure](#project-structure)

## Project Structure
```
anitrack/
├── main.py                                 # Entry point; argparser and subcommands
├── core/
│   ├── exceptions.py                       # Custom exception hierarchy
│   ├── fetcher.py                          # API fetcher
│   ├── normalizer.py                       # API Data normalizer
│   ├── file_handler.py                     # File handler for DataIO
│   └── models
│       └──anime_data_model.py              # Dataclasses: ?
└── storage
    └── *.csv                               # Saved data outputs
```

---

## Planned Features
- `get_anime_by_id`: getting data of an anime by it's id

---
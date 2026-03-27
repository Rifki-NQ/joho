from dataclasses import dataclass
from typing import Literal, get_args

DATA_SOURCES = Literal["anilist"]
VALID_DATA_SOURCES = get_args(DATA_SOURCES)

@dataclass
class AnimeDataModel:
    source: DATA_SOURCES
    id: int
    english_title: str
    romaji_title: str
    average_score: int
    episodes: int
    genres: list[str]
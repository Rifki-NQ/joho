from dataclasses import dataclass
from core.constants import DATA_SOURCES

@dataclass
class AnimeDataModel:
    source: DATA_SOURCES
    id: int
    english_title: str | None
    romaji_title: str
    average_score: int | float | None
    episodes: int | None
    genres: list[str]
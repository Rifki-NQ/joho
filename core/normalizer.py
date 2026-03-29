from core.fetcher import FetchData
from core.models.anime_model import AnimeDataModel, DATA_SOURCES, VALID_DATA_SOURCES
from core.exceptions import InvalidDataSource

class ResponseNormalizer:
    def __init__(self, fetcher: type[FetchData]) -> None:
        self.anilist_fetcher = fetcher.create_fetcher("anilist")
        
    def get_anime_data(self, source: DATA_SOURCES, anime_title: str):
        if source == "anilist":
            return self._get_anilist_data(anime_title)
        else:
            raise InvalidDataSource(f"Invalid data source provided ({source}), expected ({VALID_DATA_SOURCES})")
    
    def _get_anilist_data(self, anime_title: str):
        data = self.anilist_fetcher.fetch_data_by_title(anime_title)["data"]["Media"]
        return AnimeDataModel(
            source="anilist", id=data["id"],
            english_title=data["title"]["english"], romaji_title=data["title"]["romaji"],
            average_score=data["averageScore"], episodes=data["episodes"], genres=data["genres"]
        )
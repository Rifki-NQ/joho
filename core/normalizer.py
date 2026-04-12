from core.models.anime_model import AnimeDataModel, DATA_SOURCES, VALID_DATA_SOURCES
from core.models.protocols import FetchersProtocol
from core.exceptions import InvalidDataSource
from typing import Any

class ResponseNormalizer:
    def __init__(self, anilist_fetcher: FetchersProtocol, jikan_fetcher: FetchersProtocol) -> None:
        self.anilist_fetcher = anilist_fetcher
        self.jikan_fetcher = jikan_fetcher
        
    def get_anime_data_by_title(self, source: DATA_SOURCES, anime_title: str, entry_number: int) -> AnimeDataModel:
        self._validate_data_source(source)
        get_by_title_map = {
            "anilist": self._get_anilist_data_by_title,
            "jikan": self._get_jikan_data_by_title
        }
        return get_by_title_map[source](anime_title, entry_number)
    
    def get_anime_data_by_id(self, source: DATA_SOURCES, anime_id: int) -> AnimeDataModel:
        self._validate_data_source(source)
        get_by_id_map = {
            "anilist": self._get_anilist_data_by_id,
            "jikan": self._get_jikan_data_by_id
        }
        return get_by_id_map[source](anime_id)
    
    def get_all_anime_data_by_title(self, source: DATA_SOURCES, anime_title: str, max_entry: int | None = None) -> list[AnimeDataModel]:
        self._validate_data_source(source)
        data_source = {
            "anilist": self.anilist_fetcher.fetch_data_by_title,
            "jikan": self.jikan_fetcher.fetch_data_by_title
        }
        data_converter = {
            "anilist": self._anilist_to_anime_model,
            "jikan": self._jikan_to_anime_model
        }
        data_collection = data_source[source](anime_title)
        data_model_list: list[AnimeDataModel] = []
        for entry_num, data in enumerate(data_collection, 1):
            #inclusive for max_entry value
            if max_entry is not None and entry_num > max_entry: 
                break
            data_model_list.append(data_converter[source](data))
        return data_model_list
    
    def _get_anilist_data_by_title(self, anime_title: str, entry_number: int) -> AnimeDataModel:
        data = self.anilist_fetcher.fetch_data_by_title(anime_title)[entry_number]
        return self._anilist_to_anime_model(data)
        
    def _get_anilist_data_by_id(self, anime_id: int) -> AnimeDataModel:
        data = self.anilist_fetcher.fetch_data_by_id(anime_id)
        return self._anilist_to_anime_model(data)

    def _get_jikan_data_by_title(self, anime_title: str, entry_number: int) -> AnimeDataModel:
        data = self.jikan_fetcher.fetch_data_by_title(anime_title)[entry_number]
        return self._jikan_to_anime_model(data)
        
    def _get_jikan_data_by_id(self, anime_id: int) -> AnimeDataModel:
        data = self.jikan_fetcher.fetch_data_by_id(anime_id)
        return self._jikan_to_anime_model(data)
    
    def _anilist_to_anime_model(self, data: dict[str, Any]) -> AnimeDataModel:
        return AnimeDataModel(
            source="anilist", id=data["id"],
            english_title=data["title"]["english"], romaji_title=data["title"]["romaji"],
            average_score=data["averageScore"], episodes=data["episodes"], genres=data["genres"]
        )
    
    def _jikan_to_anime_model(self, data: dict[str, Any]) -> AnimeDataModel:
        return AnimeDataModel(
            source="jikan", id=data["mal_id"],
            english_title=data["title_english"], romaji_title=data["title"],
            average_score=data["score"], episodes=data["episodes"], genres=[g["name"] for g in data["genres"]]
        )
        
    def _validate_data_source(self, source: DATA_SOURCES) -> None:
        if source not in VALID_DATA_SOURCES:
            raise InvalidDataSource(f"Invalid data source provided ({source}), expected ({VALID_DATA_SOURCES})")
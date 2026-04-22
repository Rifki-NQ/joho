from typing import Any
from core.models.anime_model import AnimeDataModel
from core.normalizers.base_normalizer import BaseNormalizer
from core.models.protocols import FetchersProtocol
from core.constants import DEFAULT_ENTRY_INDEX

class AnilistNormalizer(BaseNormalizer):
    def __init__(self, anilist_fetcher: FetchersProtocol) -> None:
        self.anilist_fetcher = anilist_fetcher
    
    def get_anime_by_title(self, anime_title: str, entry_index: int | None = None) -> AnimeDataModel:
        if entry_index is None:
            entry_index = DEFAULT_ENTRY_INDEX
        raw_data_list = self.anilist_fetcher.fetch_data_by_title(anime_title)
        return self._anilist_to_anime_model(raw_data_list[entry_index])
    
    def get_anime_by_id(self, anime_id: int) -> AnimeDataModel:
        raw_data = self.anilist_fetcher.fetch_data_by_id(anime_id)
        return self._anilist_to_anime_model(raw_data)
    
    def get_all_anime_by_title(self, anime_title: str, max_entry: int | None = None) -> list[AnimeDataModel]:
        raw_data_list = self.anilist_fetcher.fetch_data_by_title(anime_title)
        data_model_list: list[AnimeDataModel] = []
        for entry_num, data in enumerate(raw_data_list, 1):
            #inclusive for max_entry value
            if max_entry is not None and entry_num > max_entry: 
                break
            data_model_list.append(self._anilist_to_anime_model(data))
        return data_model_list
    
    def _anilist_to_anime_model(self, data: dict[str, Any]) -> AnimeDataModel:
        return AnimeDataModel(
            source="anilist",
            id=data["id"],
            english_title=data["title"]["english"],
            romaji_title=data["title"]["romaji"],
            average_score=data["averageScore"],
            episodes=data["episodes"],
            genres=data["genres"]
        )
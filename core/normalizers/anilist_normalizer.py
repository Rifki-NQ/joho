from typing import Any, Literal
from core.models.anime_model import AnimeDataModel
from core.normalizers.base_normalizer import BaseNormalizer
from core.models.protocols import FetchersProtocol
from core.constants import DEFAULT_ENTRY_INDEX
from core.exceptions import EntryIndexError

class AnilistNormalizer(BaseNormalizer):
    def __init__(self, anilist_fetcher: FetchersProtocol) -> None:
        self.anilist_fetcher = anilist_fetcher
    
    def get_anime_by_title(self, anime_title: str, entry_index: int | None = None) -> AnimeDataModel:
        if entry_index is None:
            entry_index = DEFAULT_ENTRY_INDEX
        raw_data_list = self.anilist_fetcher.fetch_data_by_title(anime_title)
        try:
            return self._anilist_to_anime_model(raw_data_list[entry_index])
        except IndexError as e:
            raise EntryIndexError from e
    
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
            data_source="anilist",
            id=data["id"],
            romaji_title=data["title"]["romaji"],
            english_title=data["title"]["english"],
            format=data["format"],
            episodes=data["episodes"],
            status=data["status"],
            average_score=data["averageScore"],
            duration=data["duration"],
            start_date=self._get_date(data["startDate"]),
            end_date=self._get_date(data["endDate"]),
            studio=self._get_animation_studio(data["studios"]["nodes"]),
            source=data["source"],
            genres=data["genres"],
            all_time_rank=self._get_ranking("RATED", data["rankings"]),
            all_time_popularity=self._get_ranking("POPULAR", data["rankings"])
        )
        
    def _get_animation_studio(
        self,
        studio_nodes: list[dict[str, bool | str]]
        ) -> str | None:
        for node in studio_nodes:
            if node["isAnimationStudio"]:
                return str(node["name"])
        return None
    
    def _get_date(self, dates: dict[str, int]) -> str | None:
        try:
            return f"{dates['year']}-{dates['month']:02d}-{dates['day']:02d}"
        except KeyError:
            return None
        except TypeError:
            return None
        
        
    def _get_ranking(
        self,
        rank_type: Literal["RATED", "POPULAR"],
        rankings: list[dict[str, bool | str]]
        ) -> int | None:
        for rank in rankings:
            if rank["type"] == rank_type and rank["allTime"]:
                return int(rank["rank"])
        return None
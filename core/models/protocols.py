from typing import Protocol, Any
from core.models.anime_model import AnimeDataModel

class FetchersProtocol(Protocol):
    def fetch_data_by_title(self, anime_title: str) -> list[dict[str, Any]]:
        ...

    def fetch_data_by_id(self, anime_id: int) -> dict[str, Any]:
        ...
        

class NormalizerProtocol(Protocol):
    def get_anime_by_title(self, anime_title: str, entry_number: int  = 0) -> AnimeDataModel:
        ...
    
    def get_anime_by_id(self, anime_id: int, ) -> AnimeDataModel:
        ...
    
    def get_all_anime_by_title(self, anime_title: str,
                               max_entry: int | None = None) -> list[AnimeDataModel]:
        ...
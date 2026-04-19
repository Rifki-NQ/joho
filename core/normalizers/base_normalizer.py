from abc import ABC, abstractmethod
from core.models.anime_model import AnimeDataModel

DEFAULT_ENTRY_INDEX = 0

class BaseNormalizer(ABC):
    @abstractmethod
    def get_anime_by_title(self, anime_title: str, entry_index: int | None = None) -> AnimeDataModel:
        pass
    
    @abstractmethod
    def get_anime_by_id(self, anime_id: int, ) -> AnimeDataModel:
        pass
    
    @abstractmethod
    def get_all_anime_by_title(self, anime_title: str,
                               max_entry: int | None = None) -> list[AnimeDataModel]:
        pass
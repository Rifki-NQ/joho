from jikanpy import Jikan, APIException
from typing import Any
from core.fetchers.base_fetcher import FetchData, check_internet
from core.exceptions import AnimeNotFoundError

class FetchJikan(FetchData):
    def __init__(self) -> None:
        self.jikan = Jikan()
        
    def fetch_data_by_title(self, anime_title: str) -> list[dict[str, Any]]:
        anime_data = self._search_anime(anime_title)
        return anime_data
    
    @check_internet
    def fetch_data_by_id(self, anime_id: int) -> dict[str, Any]:
        try:
            return self.jikan.anime(anime_id)["data"]
        except APIException as e:
            raise AnimeNotFoundError(f"Error: requested anime not found! status code: {e.status_code}")
    
    @check_internet
    def _search_anime(self, anime_title: str) -> list[dict[str, Any]]:
        data = self.jikan.search(search_type="anime", query=anime_title)["data"]
        if not data:
            raise AnimeNotFoundError("Error: requested anime not found!")
        return data
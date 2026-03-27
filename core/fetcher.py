import requests
from abc import ABC, abstractmethod
from typing import Any
from core.models.anime_model import DATA_SOURCES, VALID_DATA_SOURCES
from core.exceptions import InvalidDataSource

class FetchData(ABC):
    
    @staticmethod
    def create_fetcher(data_source: DATA_SOURCES) -> FetchData:
        if data_source == "anilist":
            return FetchAnilist()
        else:
            raise InvalidDataSource(f"Invalid data source provided ({data_source}), expected ({VALID_DATA_SOURCES})")
        
    @abstractmethod
    def fetch_data(self, anime_title: str) -> dict[Any, Any]:
        pass
    
    def _request(self, url: str, query: str, variables: dict[str, str]) -> requests.Response:
        response = requests.post(url, json={"query": query, "variables": variables})
        return response
    
class FetchAnilist(FetchData):
    BASE_URL = "https://graphql.anilist.co"
    QUERY = """
    query ($search: String) {
        Media (search: $search, type: ANIME) {
            id
            title {
                english
                romaji
            }
            averageScore
            episodes
            genres
        }
    }
    """
    
    def fetch_data(self, anime_title: str) -> dict[Any, Any]:
        data = self._request(url=self.BASE_URL, query=self.QUERY, variables={"search": anime_title})
        return data.json()
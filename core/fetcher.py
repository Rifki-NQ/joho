import socket
import requests
from requests import ConnectionError
from jikanpy import Jikan, APIException
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, ParamSpec
from functools import wraps
from core.models.anime_model import DATA_SOURCES, VALID_DATA_SOURCES
from core.exceptions import InvalidDataSource, AppConnectionError, AnimeNotFoundError

P = ParamSpec("P")
R = TypeVar("R")

def check_internet(func: Callable[P, R]) -> Callable[P, R]:
    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        try:
            with socket.create_connection(("8.8.8.8", 53), timeout=3.0):
                pass
        except OSError:
            raise AppConnectionError(f"Failed to send requests because no internet available")
        return func(*args, **kwargs)
    return wrapper

class FetchData(ABC):
    @staticmethod
    def create_fetcher(data_source: DATA_SOURCES) -> FetchData:
        if data_source == "anilist":
            return FetchAnilist()
        elif data_source == "jikan":
            return FetchJikan()
        else:
            raise InvalidDataSource(f"Invalid data source provided ({data_source}), expected ({VALID_DATA_SOURCES})")
        
    @abstractmethod
    def fetch_data_by_title(self, anime_title: str) -> dict[Any, Any]:
        pass
    
    @abstractmethod
    def fetch_data_by_id(self, anime_id: int) -> dict[Any, Any]:
        pass
    
class FetchAnilist(FetchData):
    BASE_URL = "https://graphql.anilist.co"
    QUERY_BY_TITLE = """
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
    QUERY_BY_ID = """
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
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
    
    def fetch_data_by_title(self, anime_title: str) -> dict[Any, Any]:
        data = self._request(url=self.BASE_URL, query=self.QUERY_BY_TITLE, variables={"search": anime_title})
        media_data = data.json()["data"]["Media"]
        if media_data is None:
            raise AnimeNotFoundError("Error: requested anime not found!")
        return media_data
    
    def fetch_data_by_id(self, anime_id: int) -> dict[Any, Any]:
        data = self._request(url=self.BASE_URL, query=self.QUERY_BY_ID, variables={"id": anime_id})
        media_data = data.json()["data"]["Media"]
        if media_data is None:
            raise AnimeNotFoundError("Error: requested anime not found!")
        return media_data
    
    @check_internet
    def _request(self, url: str, query: str, variables: dict[str, str | int]) -> requests.Response:
        try:
            response = requests.post(url, json={"query": query, "variables": variables})
        except ConnectionError as e:
            raise AppConnectionError(f"Connection error occured: {e}")
        return response
    
class FetchJikan(FetchData):
    def __init__(self) -> None:
        self.jikan = Jikan()
        
    def fetch_data_by_title(self, anime_title: str) -> dict[Any, Any]:
        anime_data = self._search_anime(anime_title)
        return anime_data
    
    @check_internet
    def fetch_data_by_id(self, anime_id: int) -> dict[Any, Any]:
        try:
            return self.jikan.anime(anime_id)["data"]
        except APIException as e:
            raise AnimeNotFoundError(f"Error: requested anime not found! status code: {e.status_code}")
    
    @check_internet
    def _search_anime(self, anime_title: str) -> dict[str, Any]:
        data = self.jikan.search(search_type="anime", query=anime_title)["data"]
        if not data:
            raise AnimeNotFoundError("Error: requested anime not found!")
        return data[0] #return the first anime entry that shows up in search
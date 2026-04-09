import socket
from abc import ABC, abstractmethod
from typing import Any, Callable, TypeVar, ParamSpec
from functools import wraps
from core.exceptions import AppConnectionError

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
    @abstractmethod
    def fetch_data_by_title(self, anime_title: str) -> list[dict[Any, Any]]:
        pass
    
    @abstractmethod
    def fetch_data_by_id(self, anime_id: int) -> dict[Any, Any]:
        pass
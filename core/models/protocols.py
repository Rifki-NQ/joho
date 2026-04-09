from typing import Protocol, Any

class FetchersProtocol(Protocol):
    def fetch_data_by_title(self, anime_title: str) -> list[dict[str, Any]]:
        ...

    def fetch_data_by_id(self, anime_id: int) -> dict[str, Any]:
        ...
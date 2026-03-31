import pytest
from typing import Any
from core.fetcher import FetchData

anilist_fetcher = FetchData.create_fetcher("anilist")
anime_title = "Attack on Titan"

@pytest.fixture(scope="module")
def anilist_data() -> dict[str, Any]:
    data = anilist_fetcher.fetch_data_by_title(anime_title)
    return {
        "english_title": data["title"]["english"],
        "romaji_title": data["title"]["romaji"],
        "id": data["id"],
        "episodes": data["episodes"],
        "genres": data["genres"]
    }
    
def test_anilist_type(anilist_data: dict[str, Any]):
    assert isinstance(anilist_data["english_title"], str)
    assert isinstance(anilist_data["romaji_title"], str)
    assert isinstance(anilist_data["id"], int)
    assert isinstance(anilist_data["episodes"], int)
    assert isinstance(anilist_data["genres"], list)
    
def test_anilist_anime_title(anilist_data: dict[str, Any]):
    assert "Attack on Titan" == anilist_data["english_title"]
    assert "Shingeki no Kyojin" == anilist_data["romaji_title"]
    
def test_anilist_id(anilist_data: dict[str, Any]):
    assert 16498 == anilist_data["id"]
    
def test_anilist_episodes(anilist_data: dict[str, Any]):
    assert 25 == anilist_data["episodes"]
    
def test_anilist_genres(anilist_data: dict[str, Any]):
    assert {"Action", "Drama", "Fantasy", "Mystery"} == set(anilist_data["genres"])
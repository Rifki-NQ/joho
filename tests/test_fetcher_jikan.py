import pytest
from typing import Any
from core.fetchers.fetcher_factory import create_fetcher

jikan_fetcher = create_fetcher("jikan")
anime_title = "Attack on titan"

@pytest.fixture(scope="module")
def jikan_data() -> dict[str, Any]:
    data = jikan_fetcher.fetch_data_by_title(anime_title, entry_number=0)
    return {
        "english_title": data["title_english"],
        "romaji_title": data["title"],
        "id": data["mal_id"],
        "episodes": data["episodes"],
        "genres": [g["name"] for g in data["genres"]]
    }
    
def test_jikan_type(jikan_data: dict[str, Any]):
    assert isinstance(jikan_data["english_title"], str)
    assert isinstance(jikan_data["romaji_title"], str)
    assert isinstance(jikan_data["id"], int)
    assert isinstance(jikan_data["episodes"], int)
    assert isinstance(jikan_data["genres"], list)
    
def test_jikan_anime_title(jikan_data: dict[str, Any]):
    assert "Attack on Titan" == jikan_data["english_title"]
    assert "Shingeki no Kyojin" == jikan_data["romaji_title"]
    
def test_jikan_id(jikan_data: dict[str, Any]):
    assert 16498 == jikan_data["id"]
    
def test_jikan_episodes(jikan_data: dict[str, Any]):
    assert 25 == jikan_data["episodes"]
    
def test_jikan_genres(jikan_data: dict[str, Any]):
    assert {"Action", "Award Winning", "Drama", "Suspense"} == set(jikan_data["genres"])
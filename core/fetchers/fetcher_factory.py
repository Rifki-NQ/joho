from core.fetchers.base_fetcher import FetchData
from core.fetchers.anilist_fetcher import FetchAnilist
from core.fetchers.jikan_fetcher import FetchJikan
from core.models.anime_model import DATA_SOURCES, VALID_DATA_SOURCES
from core.exceptions import InvalidDataSource

def create_fetcher(data_source: DATA_SOURCES) -> FetchData:
    if data_source == "anilist":
        return FetchAnilist()
    elif data_source == "jikan":
        return FetchJikan()
    else:
        raise InvalidDataSource(f"Invalid data source provided ({data_source}), expected ({VALID_DATA_SOURCES})")
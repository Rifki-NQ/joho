from core.normalizers.base_normalizer import BaseNormalizer
from core.normalizers.anilist_normalizer import AnilistNormalizer
from core.normalizers.jikan_normalizer import JikanNormalizer
from core.models.protocols import FetchersProtocol
from core.constants import DATA_SOURCES, VALID_DATA_SOURCES
from core.exceptions import InvalidDataSource

def create_normalizer(source: DATA_SOURCES, fetcher: FetchersProtocol) -> BaseNormalizer:
    if source == "anilist":
        return AnilistNormalizer(fetcher)
    elif source == "jikan":
        return JikanNormalizer(fetcher)
    else:
        raise InvalidDataSource(f"Invalid data source provided ({source}), expected ({VALID_DATA_SOURCES})")
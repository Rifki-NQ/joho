import pytest
from tests.fetchers_mock_data import MockAnilistFetcher, MockJikanFetcher
from joho.core.normalizers.normalizer_factory import create_normalizer
from joho.core.models.anime_model import AnimeDataModel
from joho.core.models.protocols import NormalizerProtocol


@pytest.fixture
def anilist_normalizer() -> NormalizerProtocol:
    return create_normalizer("anilist", MockAnilistFetcher())


@pytest.fixture
def jikan_normalizer() -> NormalizerProtocol:
    return create_normalizer("jikan", MockJikanFetcher())


@pytest.fixture
def anime_data_model_anilist(anilist_normalizer: NormalizerProtocol) -> AnimeDataModel:
    return anilist_normalizer.get_anime_by_title("Attack on titan")


@pytest.fixture
def anime_data_model_jikan(jikan_normalizer: NormalizerProtocol) -> AnimeDataModel:
    return jikan_normalizer.get_anime_by_title("Attack on titan")


def test_response_normalizer_anilist_value(
    anime_data_model_anilist: AnimeDataModel,
) -> None:
    assert anime_data_model_anilist.data_source == "anilist"
    assert anime_data_model_anilist.id == 16498
    assert anime_data_model_anilist.romaji_title == "Shingeki no Kyojin"
    assert anime_data_model_anilist.english_title == "Attack on Titan"
    assert anime_data_model_anilist.format == "TV"
    assert anime_data_model_anilist.episodes == 25
    assert anime_data_model_anilist.status == "FINISHED"
    assert anime_data_model_anilist.average_score == 85
    assert anime_data_model_anilist.duration == "00:24"
    assert anime_data_model_anilist.start_date == "2013-04-07"
    assert anime_data_model_anilist.end_date == "2013-09-28"
    assert anime_data_model_anilist.studio == "WIT STUDIO"
    assert anime_data_model_anilist.source == "MANGA"
    assert anime_data_model_anilist.genres == "Action|Drama|Fantasy|Mystery"
    assert anime_data_model_anilist.all_time_rank == 73
    assert anime_data_model_anilist.all_time_popularity == 1


def test_response_normalizer_jikan_value(
    anime_data_model_jikan: AnimeDataModel,
) -> None:
    assert anime_data_model_jikan.data_source == "jikan"
    assert anime_data_model_jikan.id == 16498
    assert anime_data_model_jikan.romaji_title == "Shingeki no Kyojin"
    assert anime_data_model_jikan.english_title == "Attack on Titan"
    assert anime_data_model_jikan.format == "TV"
    assert anime_data_model_jikan.episodes == 25
    assert anime_data_model_jikan.status == "Finished Airing"
    assert anime_data_model_jikan.average_score == 8.57
    assert anime_data_model_jikan.duration == "00:24"
    assert anime_data_model_jikan.start_date == "2013-04-07"
    assert anime_data_model_jikan.end_date == "2013-09-29"
    assert anime_data_model_jikan.studio == "Wit Studio"
    assert anime_data_model_jikan.source == "Manga"
    assert anime_data_model_jikan.genres == "Action|Award Winning|Drama|Suspense"
    assert anime_data_model_jikan.all_time_rank == 125
    assert anime_data_model_jikan.all_time_popularity == 1

from typing import Any, Literal
from joho.core.models.anime_model import AnimeDataModel
from joho.core.normalizers.base_normalizer import BaseNormalizer
from joho.core.models.protocols import FetchersProtocol
from joho.core.constants import DEFAULT_ENTRY_INDEX
from joho.core.exceptions import EntryIndexError


class JikanNormalizer(BaseNormalizer):
    def __init__(self, jikan_fetcher: FetchersProtocol) -> None:
        self.jikan_fetcher = jikan_fetcher

    def get_anime_by_title(
        self, anime_title: str, entry_index: int | None = None
    ) -> AnimeDataModel:
        if entry_index is None:
            entry_index = DEFAULT_ENTRY_INDEX
        raw_data_list = self.jikan_fetcher.fetch_data_by_title(anime_title)
        try:
            return self._jikan_to_anime_model(raw_data_list[entry_index])
        except IndexError as e:
            raise EntryIndexError from e

    def get_anime_by_id(self, anime_id: int) -> AnimeDataModel:
        raw_data = self.jikan_fetcher.fetch_data_by_id(anime_id)
        return self._jikan_to_anime_model(raw_data)

    def get_all_anime_by_title(
        self, anime_title: str, max_entry: int | None = None
    ) -> list[AnimeDataModel]:
        raw_data_list = self.jikan_fetcher.fetch_data_by_title(anime_title)
        data_model_list: list[AnimeDataModel] = []
        for entry_num, data in enumerate(raw_data_list, 1):
            # inclusive for max_entry value
            if max_entry is not None and entry_num > max_entry:
                break
            data_model_list.append(self._jikan_to_anime_model(data))
        return data_model_list

    def _jikan_to_anime_model(self, data: dict[str, Any]) -> AnimeDataModel:
        return AnimeDataModel(
            data_source="jikan",
            id=data["mal_id"],
            romaji_title=data["title"],
            english_title=data["title_english"],
            format=data["type"],
            episodes=data["episodes"],
            status=data["status"],
            average_score=data["score"],
            duration=data["duration"][:2],
            start_date=self._get_date("start", data["aired"]),
            end_date=self._get_date("end", data["aired"]),
            studio=self._get_animation_studio(data["studios"]),
            source=data["source"],
            genres=self._get_genres(data["genres"]),
            all_time_rank=data["rank"],
            all_time_popularity=data["popularity"],
        )

    def _get_date(
        self, date_type: Literal["start", "end"], airing_date: dict[str, str | None]
    ) -> str | None:
        if date_type == "start" and airing_date["from"] is not None:
            return airing_date["from"][:10]
        elif date_type == "end" and airing_date["to"] is not None:
            return airing_date["to"][:10]
        return None

    def _get_animation_studio(
        self, studios: list[dict[str, str | int]] | None
    ) -> str | None:
        if not studios:
            return None
        return str(studios[0]["name"])

    def _get_genres(self, genres: list[dict[str, str | int]]) -> str:
        return "|".join([str(g["name"]) for g in genres])

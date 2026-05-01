import requests
from typing import Any
from joho.core.fetchers.base_fetcher import FetchData, check_internet
from joho.core.exceptions import AnilistError, AppConnectionError


class FetchAnilist(FetchData):
    BASE_URL = "https://graphql.anilist.co"
    QUERY_BY_TITLE = """
    query ($search: String) {
        Page (page: 1, perPage: 50) {
            media (search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                }
                format
                status
                startDate {
                    year
                    month
                    day
                }
                endDate {
                    year
                    month
                    day
                }
                episodes
                duration
                genres
                source
                averageScore
                studios {
                    nodes {
                        name
                        isAnimationStudio
                    }
                }
                rankings {
                    rank
                    type
                    allTime
                }
            }
        }
    }
    """
    QUERY_BY_ID = """
    query ($id: Int) {
        Media (id: $id, type: ANIME) {
            id
            title {
                romaji
                english
            }
            format
            status
            startDate {
                year
                month
                day
            }
            endDate {
                year
                month
                day
            }
            episodes
            duration
            genres
            source
            averageScore
            studios {
                nodes {
                    name
                    isAnimationStudio
                }
            }
            rankings {
                rank
                type
                allTime
            }
        }
    }
    """

    def fetch_data_by_title(self, anime_title: str) -> list[dict[str, Any]]:
        data = self._request(
            url=self.BASE_URL,
            query=self.QUERY_BY_TITLE,
            variables={"search": anime_title},
        )
        media_data = data.json()["data"]["Page"]["media"]
        if not media_data:
            raise AnilistError("Error: requested anime not found!")
        return media_data

    def fetch_data_by_id(self, anime_id: int) -> dict[str, Any]:
        data = self._request(
            url=self.BASE_URL, query=self.QUERY_BY_ID, variables={"id": anime_id}
        )
        media_data = data.json()["data"]["Media"]
        if not media_data:
            raise AnilistError("Error: requested anime not found!")
        return media_data

    @check_internet
    def _request(
        self, url: str, query: str, variables: dict[str, str | int]
    ) -> requests.Response:
        try:
            response = requests.post(
                url, json={"query": query, "variables": variables}, timeout=3.0
            )
        except requests.ConnectionError as e:
            raise AppConnectionError(f"Connection error occured: {e}")
        return response

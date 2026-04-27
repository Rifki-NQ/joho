from argparse import Namespace
from dataclasses import fields
from typing import Iterable, Sequence
from joho.core.cli.cli_utils import get_all_data_by_title, get_all_data_by_id
from joho.core.models.anime_model import AnimeDataModel
from joho.core.models.protocols import NormalizerProtocol
from joho.core.constants import DEFAULT_ENTRY_INDEX
from joho.core.exceptions import FetcherError, EntryIndexError


class FetchCLI:
    def handle_fetch_cli(
        self,
        args: Namespace,
        multiple_source: bool,
        normalizers: Sequence[NormalizerProtocol],
    ) -> None:
        try:
            if not multiple_source:
                self._handle_fetch_single(args, normalizers[0])
                return
            self._handle_fetch_multiple(args, normalizers)
        except FetcherError as e:
            print(e)
        except EntryIndexError:
            print(
                f"Error: out of bound entry index: {args.entry}, for title: {args.title}"
            )

    def _handle_fetch_single(
        self, args: Namespace, normalizer: NormalizerProtocol
    ) -> None:
        if args.title:
            if args.show_title:
                data_list = normalizer.get_all_anime_by_title(
                    args.title, args.max_entry
                )
                self._show_title(data_list)
                return
            data = normalizer.get_anime_by_title(args.title, args.entry)
            self._show_entry(data)
        elif args.id:
            data = normalizer.get_anime_by_id(args.id)
            self._show_entry(data)

    def _handle_fetch_multiple(
        self, args: Namespace, normalizers: Iterable[NormalizerProtocol]
    ) -> None:
        if args.title:
            data_collection = get_all_data_by_title(args, *normalizers)
            success_query = 0
            for data_list in data_collection:
                if isinstance(data_list, BaseException):
                    self._show_error(data_list)
                    break
                if args.show_title:
                    self._show_title(data_list)
                else:
                    try:
                        self._show_entry(
                            data_list[
                                DEFAULT_ENTRY_INDEX
                                if args.entry is None
                                else args.entry
                            ]
                        )
                    except IndexError as e:
                        raise EntryIndexError from e
                success_query += 1
            self._show_fetch_status(success_query, len(data_collection))
        elif args.id:
            data_list = get_all_data_by_id(args, *normalizers)
            success_query = 0
            for data in data_list:
                if isinstance(data, BaseException):
                    self._show_error(data)
                    break
                self._show_entry(data)
            self._show_fetch_status(success_query, len(data_list))

    def _show_entry(self, entry_data: AnimeDataModel) -> None:
        for f in fields(entry_data):
            value = getattr(entry_data, f.name)
            print(f"{f.name}: {value}")
        print("")

    def _show_title(self, data_list: list[AnimeDataModel]) -> None:
        print(f"Source: {data_list[0].data_source}")
        print("Romaji title | English title")
        for i, entry_data in enumerate(data_list):
            print(f"{i}. {entry_data.romaji_title} | {entry_data.english_title}")
        print("")

    def _show_error(self, error: BaseException) -> None:
        print(error)

    def _show_fetch_status(self, success: int, total_export: int) -> None:
        print(f"{success} / {total_export} fetched successfully")

from argparse import Namespace
from typing import Iterable, Sequence
from joho.core.file_handler import DataIO
from joho.core.cli.cli_utils import get_all_data_by_title, get_all_data_by_id
from joho.core.models.anime_model import AnimeDataModel
from joho.core.models.protocols import NormalizerProtocol
from joho.core.constants import DEFAULT_ENTRY_INDEX
from joho.core.exceptions import FetcherError, EntryIndexError


class ExportCLI:
    def __init__(self, file_handler: DataIO) -> None:
        self.file_handler = file_handler

    def handle_export_cli(
        self,
        args: Namespace,
        multiple_source: bool,
        normalizers: Sequence[NormalizerProtocol],
    ) -> None:
        try:
            if not multiple_source:
                self._handle_export_single(args, normalizers[0])
                return
            self._handle_export_multiple(args, normalizers)
        except FetcherError as e:
            print(e)
        except EntryIndexError:
            print(
                f"Error: out of bound entry index: {args.entry}, for title: {args.title}"
            )

    def _handle_export_single(
        self,
        args: Namespace,
        normalizer: NormalizerProtocol,
    ) -> None:
        if args.title:
            if args.save_all:
                data_list = normalizer.get_all_anime_by_title(
                    args.title, args.max_entry
                )
                self._save_data_list(args.overwrite, data_list)
                return
            data = normalizer.get_anime_by_title(args.title, args.entry)
            self._save_entry(args.overwrite, data)
        elif args.id:
            data = normalizer.get_anime_by_id(args.id)
            self._save_entry(args.overwrite, data)

    def _handle_export_multiple(
        self,
        args: Namespace,
        normalizers: Iterable[NormalizerProtocol],
    ) -> None:
        if args.title:
            data_collection = get_all_data_by_title(args, *normalizers)
            overwrite: bool = args.overwrite
            success_query = 0
            for data_list in data_collection:
                if isinstance(data_list, BaseException):
                    self._show_error(data_list)
                    continue
                if args.save_all:
                    self._save_data_list(overwrite, data_list)
                else:
                    try:
                        self._save_entry(
                            overwrite,
                            data_list[
                                DEFAULT_ENTRY_INDEX
                                if args.entry is None
                                else args.entry
                            ],
                        )
                    except IndexError as e:
                        raise EntryIndexError from e
                overwrite = False
                success_query += 1
            self._show_export_status(success_query, len(data_collection))
        elif args.id:
            data_list_by_id = get_all_data_by_id(args, *normalizers)
            success_query = 0
            for data in data_list_by_id:
                if isinstance(data, BaseException):
                    self._show_error(data)
                    continue
                self._save_entry(args.overwrite, data)
                success_query += 1
            self._show_export_status(success_query, len(data_list_by_id))

    def _save_entry(
        self,
        overwrite: bool,
        entry_data: AnimeDataModel,
    ) -> None:
        self.file_handler.save_data(entry_data, overwrite)

    def _save_data_list(
        self, overwrite: bool, data_list: Iterable[AnimeDataModel]
    ) -> None:
        for data in data_list:
            self._save_entry(overwrite, data)
            overwrite = False

    def _show_error(self, error: BaseException) -> None:
        print(error)
        print("")

    def _show_export_status(self, success: int, total_export: int) -> None:
        print(f"{success} / {total_export} exported successfully")

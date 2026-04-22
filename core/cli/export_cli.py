from argparse import Namespace
from typing import Iterable, Sequence
from core.file_handler import DataIO
from core.cli.cli_utils import get_all_data_by_title, get_all_data_by_id
from core.models.anime_model import AnimeDataModel
from core.models.protocols import NormalizerProtocol
from core.constants import DEFAULT_ENTRY_INDEX
from core.exceptions import FetcherError

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

    def _handle_export_single(
        self,
        args: Namespace,
        normalizer: NormalizerProtocol,
        ) -> None:
        if args.title:
            if args.save_all:
                all_data = normalizer.get_all_anime_by_title(args.title, args.max_entry)
                self._save_data_list(args, all_data)
                return
            data = normalizer.get_anime_by_title(args.title, args.entry)
            self._save_entry(args, data)
        elif args.id:
            data = normalizer.get_anime_by_id(args.id)
            self._save_entry(args, data)

    def _handle_export_multiple(
        self,
        args: Namespace,
        normalizers: Iterable[NormalizerProtocol],
        ) -> None:
        if args.title:
            data_collection = get_all_data_by_title(args, *normalizers)
            if args.save_all:
                self._save_data_collection(args, data_collection)
                return
            for all_data in data_collection:
                self._save_entry(
                    args,
                    all_data[DEFAULT_ENTRY_INDEX if args.entry is None else args.entry]
                    )
        elif args.id:
            all_data = get_all_data_by_id(args, *normalizers)
            self._save_data_list(args, all_data)

    def _save_entry(
        self,
        args: Namespace,
        entry_data: AnimeDataModel,
        ) -> None:
        self.file_handler.save_data(entry_data, args.path, args.overwrite)

    def _save_data_list(
        self,
        args: Namespace,
        data_list: Iterable[AnimeDataModel]
        ) -> None:
        self.file_handler.save_all_data(data_list, args.path, args.overwrite)

    def _save_data_collection(
        self,
        args: Namespace,
        data_collection: Iterable[Iterable[AnimeDataModel]]
        ) -> None:
        overwrite: bool = args.overwrite
        for data_list in data_collection:
            self.file_handler.save_all_data(
                data_list,
                args.path,
                overwrite
            )
            overwrite = False
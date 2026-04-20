from argparse import Namespace
from dataclasses import fields
from typing import Iterable
from core.cli.cli_utils import get_all_data_by_title, get_all_data_by_id
from core.models.anime_model import AnimeDataModel
from core.models.protocols import NormalizerProtocol
from core.exceptions import FetcherError

DEFAULT_ENTRY_INDEX = 0

def fetch_cli(args: Namespace, multiple_source: bool, *normalizers: NormalizerProtocol) -> None:
    try:
        if not multiple_source:
            _handle_fetch_single(args, normalizers[0])
            return
        _handle_fetch_multiple(args, normalizers)
    except FetcherError as e:
        print(e)

def _handle_fetch_single(args: Namespace, normalizer: NormalizerProtocol) -> None:
    if args.title:
        if args.show_title:
            all_data = normalizer.get_all_anime_by_title(args.title, args.max_entry)
            _show_title(all_data)
            return
        data = normalizer.get_anime_by_title(args.title, args.entry)
        _show_entry(data)
    elif args.id:
        data = normalizer.get_anime_by_id(args.id)
        _show_entry(data)

def _handle_fetch_multiple(args: Namespace, normalizers: Iterable[NormalizerProtocol]) -> None:
    if args.title:
        data_collection = get_all_data_by_title(args, *normalizers)
        if args.show_title:
            for all_data in data_collection:
                _show_title(all_data)
            return
        for all_data in data_collection:
            _show_entry(all_data[DEFAULT_ENTRY_INDEX if args.entry is None else args.entry])
    elif args.id:
        all_data = get_all_data_by_id(args, *normalizers)
        for data in all_data:
            _show_entry(data)

def _show_entry(entry_data: AnimeDataModel) -> None:
    for f in fields(entry_data):
        value = getattr(entry_data, f.name)
        print(f"{f.name}: {value}")

def _show_title(all_data: list[AnimeDataModel]) -> None:
    for entry_data in all_data:
        print(f"Source: {entry_data.source}")
        print("Romaji title | English title")
        print(f"{entry_data.romaji_title} | {entry_data.english_title}")
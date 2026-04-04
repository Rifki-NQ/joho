import argparse
from dataclasses import asdict
from core.normalizer import ResponseNormalizer
from core.file_handler import DataIO
from core.exceptions import FetcherError

class ExportCLI:
    def __init__(self, normalizer: ResponseNormalizer, file_handler: DataIO) -> None:
        self.file_handler = file_handler
        self.normalizer = normalizer
        
    def handle_export(self, args: argparse.Namespace) -> None:
        if args.title: #search by title
            try:
                data = asdict(self.normalizer.get_anime_data_by_title(source=args.source, anime_title=args.title))
            except FetcherError as e:
                print(e)
                return
                
        elif args.id: #search by id
            try:
                data = asdict(self.normalizer.get_anime_data_by_id(source=args.source, anime_id=args.id))
            except FetcherError as e:
                print(e)
                return
        else:
            raise AssertionError("unreachable: argparse guarantees --title or --id")
        
        self.file_handler.add_new_data(new_data=data, filepath=args.path, overwrite=args.overwrite)
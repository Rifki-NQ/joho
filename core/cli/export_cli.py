from argparse import Namespace
from dataclasses import asdict
from core.normalizer import ResponseNormalizer
from core.file_handler import DataIO
from core.utils import get_all_data
from core.exceptions import FetcherError

class ExportCLI:
    def __init__(self, normalizer: ResponseNormalizer, file_handler: DataIO) -> None:
        self.file_handler = file_handler
        self.normalizer = normalizer
        
    def handle_export(self, args: Namespace) -> None:
        if args.title: #search by title
            try:
                if args.source == "all":
                    data1, data2 = get_all_data("title", args, self.normalizer)
                    data_collection = (data1, data2)
                    for data in data_collection:
                        self.file_handler.add_new_data(new_data=data, filepath=args.path, overwrite=args.overwrite)
                else:
                    data = asdict(self.normalizer.get_anime_data_by_title(source=args.source, anime_title=args.title, entry_number=args.entry))
                    self.file_handler.add_new_data(new_data=data, filepath=args.path, overwrite=args.overwrite)
            except FetcherError as e:
                print(e)
                return
                
        elif args.id: #search by id
            try:
                if args.source == "all":
                    data1, data2 = get_all_data("id", args, self.normalizer)
                    data_collection = (data1, data2)
                    for data in data_collection:
                        self.file_handler.add_new_data(new_data=data, filepath=args.path, overwrite=args.overwrite)
                else:
                    data = asdict(self.normalizer.get_anime_data_by_id(source=args.source, anime_id=args.id))
                    self.file_handler.add_new_data(new_data=data, filepath=args.path, overwrite=args.overwrite)
            except FetcherError as e:
                print(e)
                return
        else:
            raise AssertionError("unreachable: argparse guarantees --title or --id")
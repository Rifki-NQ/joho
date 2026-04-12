from argparse import Namespace
from core.normalizer import ResponseNormalizer
from core.file_handler import DataIO
from core.cli.cli_utils import get_all_data_by_title, get_all_data_by_id
from core.exceptions import FetcherError

class ExportCLI:
    def __init__(self, normalizer: ResponseNormalizer, file_handler: DataIO) -> None:
        self.file_handler = file_handler
        self.normalizer = normalizer
        
    def handle_export(self, args: Namespace) -> None:
        if args.title: #search by title
            self._handle_args_title(args)
                
        elif args.id: #search by id
            self._handle_args_id(args)
        
    def _handle_args_title(self, args: Namespace) -> None:
        try:
            if args.source == "all": #handle --source all
                self._handle_source_all_by_title(args)
            elif args.save_all: #handle --save-all flag
                data_list = self.normalizer.get_all_anime_data_by_title(args.source, args.title)
                self.file_handler.save_all_data(data_list, args.path, args.overwrite)
            else:
                data = self.normalizer.get_anime_data_by_title(args.source, args.title, args.entry)
                self.file_handler.save_data(data, args.path, args.overwrite)
        except FetcherError as e:
            print(e)
        except IndexError:
            print(f"Error: --entry index out of range for title: {args.title}")
        
    def _handle_args_id(self, args: Namespace) -> None:
        try:
            if args.source == "all": #handle --source all
                self._handle_source_all_by_id(args)
            else:
                data = self.normalizer.get_anime_data_by_id(args.source, args.id)
                self.file_handler.save_data(data, args.path, args.overwrite)
        except FetcherError as e:
            print(e)
            return
        
    def _handle_source_all_by_title(self, args: Namespace) -> None:
        data_collection = get_all_data_by_title(args, self.normalizer)
        for data_list in data_collection:
            #handle --save-all flag
            if args.save_all:
                self.file_handler.save_all_data(data_list, args.path, args.overwrite)
            #handle --entry
            else:
                entry: int = args.entry
                self.file_handler.save_data(data_list[entry], args.path, args.overwrite)
            args.overwrite = False

    def _handle_source_all_by_id(self, args: Namespace) -> None:
        data_list = get_all_data_by_id(args, self.normalizer)
        self.file_handler.save_all_data(data_list, args.path, args.overwrite)
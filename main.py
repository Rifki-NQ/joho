import argparse
from core.cli.fetch_cli import FetchCLI
from core.cli.export_cli import ExportCLI
from core.fetchers.fetcher_factory import create_fetcher
from core.normalizer import ResponseNormalizer
from core.file_handler import valid_filepath
from core.file_handler import DataIO

class Main:
    def __init__(self) -> None:
        self.anilist_fetcher = create_fetcher("anilist")
        self.jikan_fetcher = create_fetcher("jikan")
        
        self.response_normalizer = ResponseNormalizer(self.anilist_fetcher, self.jikan_fetcher)
        self.file_handler = DataIO()
        
        self.fetch_cli = FetchCLI(self.response_normalizer)
        self.export_cli = ExportCLI(self.response_normalizer, self.file_handler)
    
    def main_parser(self):
        parser = argparse.ArgumentParser(prog="anitrack")
        subparsers = parser.add_subparsers(dest="command")

        #subcommand fetch
        fetch_parser = subparsers.add_parser("fetch", description="fetch anime data")
        fetch_parser.add_argument("--source", choices={"anilist", "jikan", "all"}, required=True)
        fetch_parser.add_argument("--max-entry", type=int, default=None)

        fetch_entry_group = fetch_parser.add_mutually_exclusive_group(required=False)
        fetch_entry_group.add_argument("--entry", type=int, default=None)
        fetch_entry_group.add_argument("--show-title", action="store_true", default=False)
        
        search_by_group = fetch_parser.add_mutually_exclusive_group(required=True)
        search_by_group.add_argument("--title", type=str)
        search_by_group.add_argument("--id", type=int)
        
        #subcommand export
        export_parser =subparsers.add_parser("export", description="fetch then save anime data")
        export_parser.add_argument("--source", choices={"anilist", "jikan", "all"}, required=True)

        search_by_group = export_parser.add_mutually_exclusive_group(required=True)
        search_by_group.add_argument("--title", type=str)
        search_by_group.add_argument("--id", type=int)

        export_entry_group = export_parser.add_mutually_exclusive_group(required=False)
        export_entry_group.add_argument("--entry", type=int, default=0)
        export_entry_group.add_argument("--save-all", action="store_true", default=False)

        export_parser.add_argument("--path", type=valid_filepath, required=True)
        export_parser.add_argument("--overwrite", action="store_true", default=False)
        export_parser.add_argument("--max-entry", type=int, default=None)

        args = parser.parse_args()
        
        if args.command == "fetch":
            if args.title is None and (args.entry is not None or args.show_title):
                fetch_parser.error("--entry and --show-title can only be used with --title")
            elif args.max_entry is not None and not args.show_title:
                fetch_parser.error("--max-entry can only be used with --show-title")
            self.fetch_cli.handle_fetch(args)
            
        elif args.command == "export":
            if args.title is None and (args.entry is not None or args.save_all):
                export_parser.error("--entry and --save-all can only be used with --title")
            elif args.max_entry is not None and not args.save_all:
                export_parser.error("--max-entry can only be used with --save-all")
            self.export_cli.handle_export(args)
        else:
            parser.print_help()
            
if __name__ == "__main__":
    main = Main()
    main.main_parser()
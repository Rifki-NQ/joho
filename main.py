import argparse
from core.cli.fetch_cli import FetchCLI
from core.cli.export_cli import ExportCLI
from core.fetcher import FetchData
from core.normalizer import ResponseNormalizer
from core.file_handler import valid_filepath
from core.file_handler import DataIO

class Main:
    def __init__(self) -> None:
        self.anilist_fetcher = FetchData.create_fetcher("anilist")
        self.jikan_fetcher = FetchData.create_fetcher("jikan")
        
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
        fetch_parser.add_argument("--entry", type=int, default=0)
        
        fetch_group = fetch_parser.add_mutually_exclusive_group(required=True)
        fetch_group.add_argument("--title", type=str)
        fetch_group.add_argument("--id", type=int)
        
        #subcommand export
        export_parser =subparsers.add_parser("export", description="fetch then save anime data")
        export_parser.add_argument("--source", choices={"anilist", "jikan"}, required=True)
        export_parser.add_argument("--entry", type=int, default=0)

        export_group = export_parser.add_mutually_exclusive_group(required=True)
        export_group.add_argument("--title", type=str)
        export_group.add_argument("--id", type=int)

        export_parser.add_argument("--path", type=valid_filepath, required=True)
        export_parser.add_argument("--overwrite", action="store_true", default=False)

        args = parser.parse_args()

        if args.command == "fetch":
            self.fetch_cli.handle_fetch(args)
        elif args.command == "export":
            self.export_cli.handle_export(args)
        else:
            parser.print_help()
            
if __name__ == "__main__":
    main = Main()
    main.main_parser()
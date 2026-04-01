import argparse
from core.cli.fetch_cli import FetchCLI
from core.models.anime_model import VALID_DATA_SOURCES
from core.fetcher import FetchData
from core.normalizer import ResponseNormalizer

class Main:
    def __init__(self) -> None:
        self.anilist_fetcher = FetchData.create_fetcher("anilist")
        self.jikan_fetcher = FetchData.create_fetcher("jikan")
        self.response_normalizer = ResponseNormalizer(self.anilist_fetcher, self.jikan_fetcher)
        self.fetch_cli = FetchCLI(self.response_normalizer)
    
    def main_parser(self):
        parser = argparse.ArgumentParser(prog="anitrack")
        subparsers = parser.add_subparsers(dest="command")

        #subcommand fetch
        fetch_parser = subparsers.add_parser("fetch", description="fetch anime data")
        fetch_parser.add_argument("--source", choices=VALID_DATA_SOURCES, required=True)
        
        group = fetch_parser.add_mutually_exclusive_group(required=True)
        group.add_argument("--title", type=str)
        group.add_argument("--id", type=int)

        args = parser.parse_args()

        if args.command == "fetch":
            self.fetch_cli.handle_fetch(args)
        else:
            parser.print_help()
            
if __name__ == "__main__":
    main = Main()
    main.main_parser()
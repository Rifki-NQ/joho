import argparse
from dataclasses import asdict
from core.normalizer import ResponseNormalizer

class FetchCLI:
    def __init__(self, normalizer: ResponseNormalizer) -> None:
        self.normalizer = normalizer
    
    def handle_fetch(self, args: argparse.Namespace) -> None:
        if args.title: #search by title
            data = asdict(self.normalizer.get_anime_data_by_title(source=args.source, anime_title=args.title))
            for key, value in data.items():
                print(f"{key}: {value}")
                
        elif args.id: #search by id
            data = asdict(self.normalizer.get_anime_data_by_id(source=args.source, anime_id=args.id))
            for key, value in data.items():
                print(f"{key}: {value}")
from argparse import Namespace
from dataclasses import asdict, fields
from core.normalizer import ResponseNormalizer
from core.exceptions import FetcherError
from core.utils import get_all_data
from core.models.anime_model import AnimeDataModel

class FetchCLI:
    def __init__(self, normalizer: ResponseNormalizer) -> None:
        self.normalizer = normalizer
    
    def handle_fetch(self, args: Namespace) -> None:
        if args.title: #search by title
            try:
                if args.source == "all":
                    data1, data2 = get_all_data("title", args, self.normalizer)
                    for f in fields(AnimeDataModel):
                        print(f"{f.name}: {data1[f.name]} | {data2[f.name]}")
                else:
                    data = asdict(self.normalizer.get_anime_data_by_title(source=args.source, anime_title=args.title, entry_number=args.entry))
                    for key, value in data.items():
                        print(f"{key}: {value}")
            except FetcherError as e:
                print(e)
                return
                
        elif args.id: #search by id
            try:
                if args.source == "all":
                    data1, data2 = get_all_data("id", args, self.normalizer)
                    for f in fields(AnimeDataModel):
                        print(f"{f.name}: {data1[f.name]} | {data2[f.name]}")
                else:
                    data = asdict(self.normalizer.get_anime_data_by_id(source=args.source, anime_id=args.id))
                    for key, value in data.items():
                        print(f"{key}: {value}")
            except FetcherError as e:
                print(e)
                return
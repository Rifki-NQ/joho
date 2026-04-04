import argparse
from dataclasses import asdict, fields
from core.normalizer import ResponseNormalizer
from core.exceptions import FetcherError
from core.models.anime_model import AnimeDataModel

class FetchCLI:
    def __init__(self, normalizer: ResponseNormalizer) -> None:
        self.normalizer = normalizer
    
    def handle_fetch(self, args: argparse.Namespace) -> None:
        if args.title: #search by title
            try:
                if args.source == "all":
                    data1 = asdict(self.normalizer.get_anime_data_by_title(source="anilist", anime_title=args.title))
                    data2 = asdict(self.normalizer.get_anime_data_by_title(source="jikan", anime_title=args.title))
                    for f in fields(AnimeDataModel):
                        print(f"{f.name}: {data1[f.name]} | {data2[f.name]}")
                    return
                
                data = asdict(self.normalizer.get_anime_data_by_title(source=args.source, anime_title=args.title))
            except FetcherError as e:
                print(e)
                return
            
            for key, value in data.items():
                print(f"{key}: {value}")
                
        elif args.id: #search by id
            try:
                if args.source == "all":
                    data1 = asdict(self.normalizer.get_anime_data_by_id(source="anilist", anime_id=args.id))
                    data2 = asdict(self.normalizer.get_anime_data_by_id(source="jikan", anime_id=args.id))
                    for f in fields(AnimeDataModel):
                        print(f"{f.name}: {data1[f.name]} | {data2[f.name]}")
                    return
                
                data = asdict(self.normalizer.get_anime_data_by_id(source=args.source, anime_id=args.id))
            except FetcherError as e:
                print(e)
                return
            
            for key, value in data.items():
                print(f"{key}: {value}")
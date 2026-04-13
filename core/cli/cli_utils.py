from argparse import Namespace
import asyncio
from core.models.anime_model import AnimeDataModel
from core.normalizer import ResponseNormalizer

def get_all_data_by_title(args: Namespace, normalizer: ResponseNormalizer) -> tuple[list[AnimeDataModel], list[AnimeDataModel]]:
    return asyncio.run(_get_all_by_title(args, normalizer))

def get_all_data_by_id(args: Namespace, normalizer: ResponseNormalizer) -> tuple[AnimeDataModel, AnimeDataModel]:
    return asyncio.run(_get_all_by_id(args, normalizer))

async def _get_all_by_title(args: Namespace, normalizer: ResponseNormalizer) -> tuple[list[AnimeDataModel], list[AnimeDataModel]]:
        anilist_data, jikan_data = await asyncio.gather(asyncio.to_thread(lambda: normalizer.get_all_anime_data_by_title(
                                                                          source="anilist", anime_title=args.title, max_entry=args.max_entry)),
                                                        asyncio.to_thread(lambda: normalizer.get_all_anime_data_by_title(
                                                                          source="jikan", anime_title=args.title, max_entry=args.max_entry)))
        return anilist_data, jikan_data
    
async def _get_all_by_id(args: Namespace, normalizer: ResponseNormalizer) -> tuple[AnimeDataModel, AnimeDataModel]:
        anilist_data, jikan_data = await asyncio.gather(asyncio.to_thread(lambda: normalizer.get_anime_data_by_id(
                                                                          source="anilist", anime_id=args.id)),
                                                        asyncio.to_thread(lambda: normalizer.get_anime_data_by_id(
                                                                          source="jikan", anime_id=args.id)))
        return anilist_data, jikan_data
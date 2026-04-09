from argparse import Namespace
import asyncio
from dataclasses import asdict
from typing import Any, Literal
from core.normalizer import ResponseNormalizer

def get_all_data(by: Literal["title", "id"],args: Namespace, normalizer: ResponseNormalizer) -> tuple[dict[str, Any], dict[str, Any]]:
    if by == "id":
        return asyncio.run(_get_all_by_id(args, normalizer))
    elif by == "title":
        return asyncio.run(_get_all_by_title(args, normalizer))
    raise ValueError(f"Invalid argument given for 'by': {by}, expected: title or id")

async def _get_all_by_title(args: Namespace, normalizer: ResponseNormalizer) -> tuple[dict[str, Any], dict[str, Any]]:
        anilist_data, jikan_data = await asyncio.gather(asyncio.to_thread(lambda: normalizer.get_anime_data_by_title(
                                                                          source="anilist", anime_title=args.title, entry_number=args.entry)),
                                                        asyncio.to_thread(lambda: normalizer.get_anime_data_by_title(
                                                                          source="jikan", anime_title=args.title, entry_number=args.entry)))
        return asdict(anilist_data), asdict(jikan_data)
    
async def _get_all_by_id(args: Namespace, normalizer: ResponseNormalizer) -> tuple[dict[str, Any], dict[str, Any]]:
        anilist_data, jikan_data = await asyncio.gather(asyncio.to_thread(lambda: normalizer.get_anime_data_by_id(
                                                                          source="anilist", anime_id=args.id)),
                                                        asyncio.to_thread(lambda: normalizer.get_anime_data_by_id(
                                                                          source="jikan", anime_id=args.id)))
        return asdict(anilist_data), asdict(jikan_data)
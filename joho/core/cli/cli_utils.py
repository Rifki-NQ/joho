from argparse import Namespace
import asyncio
from joho.core.models.anime_model import AnimeDataModel
from joho.core.models.protocols import NormalizerProtocol


def get_all_data_by_title(
    args: Namespace, *normalizers: NormalizerProtocol
) -> list[list[AnimeDataModel] | BaseException]:
    return asyncio.run(_get_all_by_title(args, *normalizers))


def get_all_data_by_id(
    args: Namespace, *normalizers: NormalizerProtocol
) -> list[AnimeDataModel | BaseException]:
    return asyncio.run(_get_all_by_id(args, *normalizers))


async def _get_all_by_title(
    args: Namespace, *normalizers: NormalizerProtocol
) -> list[list[AnimeDataModel] | BaseException]:
    all_thread = [
        asyncio.to_thread(normalizer.get_all_anime_by_title, args.title, args.max_entry)
        for normalizer in normalizers
    ]
    all_data = await asyncio.gather(*all_thread, return_exceptions=True)
    return all_data


async def _get_all_by_id(
    args: Namespace, *normalizers: NormalizerProtocol
) -> list[AnimeDataModel | BaseException]:
    all_thread = [
        asyncio.to_thread(normalizer.get_anime_by_id, args.id)
        for normalizer in normalizers
    ]
    all_data = await asyncio.gather(*all_thread, return_exceptions=True)
    return all_data

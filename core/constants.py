from typing import Literal, get_args

DATA_SOURCES = Literal["anilist", "jikan"]
VALID_DATA_SOURCES = get_args(DATA_SOURCES)

DEFAULT_ENTRY_INDEX = 0
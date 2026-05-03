class AppError(Exception):
    """Base class exception for all app related error"""

    pass


class FetcherError(AppError):
    """Raised when there is fetcher related error"""

    pass


class InvalidDataSource(FetcherError):
    """Raised when the data source is invalid"""

    pass


class AppConnectionError(FetcherError):
    """Raised when there is connection related error"""

    pass


class AnilistError(FetcherError):
    """Raised when Anilist error occured"""

    pass


class JikanError(FetcherError):
    """Raised when Jikan error occured"""

    pass


class EntryIndexError(AppError):
    """Raised when the entry index is out of bound"""

    pass


class FileHandlerError(AppError):
    """Raised when there is file handler related error"""

    pass


class FileNotExistError(FileHandlerError):
    """Raised when the file does not exist"""

    pass


class FileEmptyError(FileHandlerError):
    """Raised when the file contains empty data"""

    pass


class MissingHeaderError(FileHandlerError):
    """Raised when the file contains data that is missing some header"""

    pass


class InvalidHeaderError(FileHandlerError):
    """Raised when the file contains data with invalid or unexpected header"""

    pass

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
    """Raised when there is connection relarted error"""
    pass

class AnimeNotFoundError(FetcherError):
    """Raised when the requested anime is not found"""
    pass
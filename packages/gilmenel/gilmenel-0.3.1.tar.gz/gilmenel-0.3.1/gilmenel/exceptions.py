class AsteriaError(Exception):
    """Base class for exceptions in this module."""

    pass


class CatalogUnavailableError(AsteriaError):
    """Raised when the requested catalogue is not available."""

    pass


class NoStarsFoundError(AsteriaError):
    """Raised when no stars are returned in field."""

    pass

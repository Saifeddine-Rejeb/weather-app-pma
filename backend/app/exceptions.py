class GeocodingError(Exception):
    """Raised when a location cannot be geocoded."""

    pass


class WeatherClientError(Exception):
    """Raised when the weather API returns an error."""

    pass


class RecordNotFoundError(Exception):
    """Raised when a weather record ID does not exist."""

    pass


class InvalidDateRangeError(ValueError):
    """Raised when start_date > end_date or date format is wrong."""

    pass


class ExternalAPIError(Exception):
    """Raised when a third-party API (YouTube, Maps, AQI) fails."""

    pass

import logging
from pydantic import AnyHttpUrl

from src.core.exceptions import TrackSourceNotFound
from src.services.constants import TrackSource


logger = logging.getLogger(__name__)


def track_source_parser(track_url: AnyHttpUrl) -> TrackSource:
    """Parse source of the track

    Args:
        track_url (AnyHttpUrl): Track url

    Returns:
        TrackSource: Source enum value
    """
    if 'yandex' in track_url:
        return TrackSource.YANDEX_MUSIC

    elif 'youtube' in track_url or 'youtu.be' in track_url:
        return TrackSource.YOUTUBE

    else:
        error_message = f'Not found source for: {track_url}'
        logger.error(error_message)
        raise TrackSourceNotFound(error_message)

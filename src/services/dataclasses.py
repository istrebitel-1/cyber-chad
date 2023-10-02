from dataclasses import dataclass
from typing import Dict

from src.services.constants import TrackSource


TrackSourceT = TrackSource | str


@dataclass
class TrackInfo:
    """Dataclass Track info"""
    url: str
    title: str
    source: TrackSource
    extra: Dict | None = None

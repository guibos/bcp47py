"""Module related with BCP47Type enum"""
from enum import Enum


class BCP47Type(Enum):
    """Enum that contains names of all bcp47 subtag types."""
    LANGUAGE = 'language'
    SCRIPT = 'script'
    REGION = 'region'
    VARIANT = 'variant'
    GRANDFATHERED = 'grandfathered'
    REDUNDANT = 'redundant'
    EXTLANG = 'extlang'

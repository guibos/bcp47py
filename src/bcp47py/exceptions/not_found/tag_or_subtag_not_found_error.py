import abc
from abc import ABC

from enums.bcp47_type import BCP47Type


class TagOrSubtagNotFoundError(ABC, Exception):
    """Some tag or subtag is not found."""


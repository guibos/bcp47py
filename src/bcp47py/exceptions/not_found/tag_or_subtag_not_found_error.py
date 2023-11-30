from abc import ABC


class TagOrSubtagNotFoundError(ABC, Exception):
    """Some tag or subtag is not found."""

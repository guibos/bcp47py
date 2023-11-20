"""Module related with LanguageScopeEnum."""
import enum


class LanguageScopeEnum(enum.Enum):
    """Scopes are contained by a primary or extended language subtag indicating the type of language code according to
    ISO 639."""
    COLLECTION = 'collection'
    PRIVATE_USE = 'private-use'
    MACRO_LANGUAGE = 'macrolanguage'
    SPECIAL = 'special'

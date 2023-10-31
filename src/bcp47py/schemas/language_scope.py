"""Module related with LanguageScope."""
from pydantic import BaseModel

from enums.language_scope import LanguageScopeEnum


class LanguageScope(BaseModel):
    """Scopes are contained by a primary or extended language subtag indicating the type of language code according to
    ISO 639. The values permitted in this field are "macrolanguage", "collection", "special", and "private-use".
    When this field is omitted by a primary or extended language subtag is an individual language."""
    scope: LanguageScopeEnum

from pydantic import BaseModel

from enums.language_scope import LanguageScopeEnum


class LanguageScope(BaseModel):
    scope: LanguageScopeEnum

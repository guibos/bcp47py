from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel, field_validator
from pydantic_core.core_schema import ValidationInfo

from schemas.mixin.subtag import Subtag
from schemas.language import Language


class ExtLangPreferredValue(BaseModel):
    language: Optional[Language] = None
    model_config = ConfigDict(extra='forbid')


class ExtLangPrefix(BaseModel):
    language: Language

    @property
    def tag(self) -> str:
        return self.language.subtag

    model_config = ConfigDict(extra='forbid')


class ExtLang(Subtag):
    preferred_value: ExtLangPreferredValue
    prefix: List[ExtLangPrefix] = []
    macro_language: Optional[Language] = None
    deprecated: Optional[datetime] = None

    @field_validator('preferred_value')
    def preferred_value_subtag_validator(cls, value: Language, validation_info: ValidationInfo):
        if value.language.subtag != validation_info.data['subtag']:
            raise ValueError('Preferred_value must be equal than subtag. In the moment of writing this validation all'
                             'extension languages are languages, so, it is possible that this validation it is not '
                             'necessary any more.')
        return value

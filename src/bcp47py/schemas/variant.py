from datetime import datetime
from typing import List, Optional

from pydantic import ConfigDict, BaseModel

from schemas.abstract.subtag import Subtag
from schemas.abstract.preferred_value_validator import PreferredValueValidator
from schemas.ext_lang import ExtLangPrefix, ExtLang
from schemas.region import Region
from schemas.script import Script


class VariantPreferredValue(BaseModel):
    variant: 'Variant'
    model_config = ConfigDict(extra='forbid')


class VariantPrefix(ExtLangPrefix):
    ext_lang: Optional[ExtLang] = None
    script: Optional[Script] = None
    region: Optional[Region] = None
    variant: Optional['Variant'] = None

    @property
    def tag(self) -> str:
        return '-'.join((subtag.subtag
                         for subtag in (self.language, self.ext_lang, self.script, self.region, self.variant)
                         if subtag))


class Variant(Subtag, PreferredValueValidator):
    prefix: List[VariantPrefix] = []
    comments: Optional[str] = None
    preferred_value: Optional[VariantPreferredValue] = None
    deprecated: Optional[datetime] = None

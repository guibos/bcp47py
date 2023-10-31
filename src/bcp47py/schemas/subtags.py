"""Module related with Subtags wrapper class."""
from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from schemas.ext_lang import ExtLang
from schemas.language import Language
from schemas.region import Region
from schemas.script import Script
from schemas.variant import Variant


class Subtags(BaseModel):
    """Helper that have attributes for each subtag of a Tag."""
    language: Language
    ext_lang: List[ExtLang]
    script: Optional[Script] = None
    region: Optional[Region] = None
    variant: Optional[Variant] = None

    @property
    def tag(self) -> str:
        """Return a tag in string format."""
        return '-'.join((subtag.subtag
                         for subtag in (self.language, '-'.join(self.ext_lang), self.script, self.region, self.variant)
                         if subtag))

    def __hash__(self):
        return hash(str(self.tag))

    def __eq__(self, other: 'Subtags'):
        return self.tag == other.tag

    model_config = ConfigDict(extra='forbid')

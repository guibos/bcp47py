"""Module related with Grandfathered classes."""
from datetime import datetime
from typing import Optional, List, Annotated

from pydantic import ConfigDict, BaseModel

from schemas.abstract.preferred_value import PreferredValue
from schemas.field_info import COMMENTS_FIELD_INFO
from schemas.mixin.tag import Tag
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.language import Language
from schemas.region import Region
from schemas.variant import Variant


class GrandfatheredPreferredValue(PreferredValue):
    """Class that adds :class:`bcp47py.schemas.language.Language`, :class:`bcp47py.schemas.region.Region` and
    :class:`bcp47py.schemas.variant.Variant` attributes that could be set as preferred value for a
    :class:`bcp47py.schemas.grandfathered.Grandfathered` type.

    Check :class:`bcp47py.schemas.abstract.preferred_value.PreferredValue` class for more information about preferred value."""
    language: Language
    region: Optional[Region] = None
    variant: Optional[Variant] = None
    model_config = ConfigDict(extra='forbid')

    def tag(self):
        return '-'.join([subtag.subtag for subtag in [self.language, self.region, self.variant] if subtag])


class Grandfathered(Tag, PreferredValueValidator):
    """Prior to RFC 4646, whole language tags were registered according to the rules in RFC 1766 and/or RFC 3066. All
    of these registered tags remain valid as language tags.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []
    preferred_value: Optional['GrandfatheredPreferredValue'] = None
    deprecated: Optional[datetime] = None

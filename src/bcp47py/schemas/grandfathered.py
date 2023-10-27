from datetime import datetime
from typing import Optional, List

from pydantic import ConfigDict, BaseModel

from schemas.abstract.preferred_value import PreferredValue
from schemas.mixin.tag import Tag
from schemas.mixin.preferred_value_validator import PreferredValueValidator
from schemas.language import Language
from schemas.region import Region
from schemas.variant import Variant


class GrandfatheredPreferredValue(PreferredValue):
    """Class that implements language, region and variant that could be set as preferred value from a Grandfathered
    type.

    Check :class:schemas.abstract.preferred_value.PreferredValue class for more information about preferred value."""
    language: Language
    region: Optional[Region] = None
    variant: Optional[Variant] = None
    model_config = ConfigDict(extra='forbid')

    def tag(self):
        return '-'.join([subtag.subtag for subtag in [self.language, self.region, self.variant] if subtag])


class Grandfathered(Tag, PreferredValueValidator):
    """Prior to RFC 4646, whole language tags were registered according to the rules in RFC 1766 and/or RFC 3066. All
    of these registered tags remain valid as language tags.

    Many of these registered tags were made redundant by the advent of either RFC 4646 or this document. A redundant
    tag is a grandfathered registration whose individual subtags appear with the same semantic meaning in the registry.
    For example, the tag "zh-Hant" (Traditional Chinese) can now be composed from the subtags 'zh' (Chinese) and 'Hant'
    (Han script traditional variant). These redundant tags are maintained in the registry as records of type
    'redundant', mostly as a matter of historical curiosity.

    The remainder of the previously registered tags are "grandfathered". These tags are classified into two groups:
    'regular' and 'irregular'.

    Grandfathered tags that (appear to) match the 'langtag' production in Figure 1 are considered 'regular'
    grandfathered tags. These tags contain one or more subtags that either do not individually appear in the registry
    or appear but with a different semantic meaning: each tag, in its entirety, represents a language or collection of
    languages.

    Grandfathered tags that do not match the 'langtag' production in the ABNF and would otherwise be invalid are
    considered 'irregular' grandfathered tags. With the exception of "en-GB-oed", which is a variant of "en-GB", each
    of them, in its entirety, represents a language.

    Many of the grandfathered tags have been superseded by the subsequent addition of new subtags: each superseded
    record contains a 'Preferred-Value' field that ought to be used to form language tags representing that value. For
    example, the tag "art-lojban" is superseded by the primary language subtag 'jbo'."""
    comments: Optional[str] = None
    preferred_value: Optional['GrandfatheredPreferredValue'] = None
    deprecated: Optional[datetime] = None

from datetime import datetime
from typing import List, Optional, Annotated

from pydantic import field_validator
from pydantic_core.core_schema import ValidationInfo

from schemas.abstract.preferred_value import PreferredValue
from schemas.abstract.prefix import Prefix
from schemas.mixin.subtag import Subtag
from schemas.language import Language
from schemas.field_info import DEPRECATED_FIELD_INFO, MACRO_LANGUAGE_FIELD_INFO


class ExtLangPreferredValue(PreferredValue):
    """Class that implements the only subtag, language, that could be set as preferred value from an ExtLang type.

    Check :class:schemas.abstract.preferred_value.PreferredValue class for more information about preferred value."""
    language: Language

    @property
    def tag(self) -> str:
        return self.language.subtag


class ExtLangPrefix(Prefix):
    """Class that implements the only subtag, language, that could be set as preferred value from an ExtLang type.

    check :class:schemas.abstract.prefix.Prefix class for more information about prefix."""
    language: Language

    @property
    def tag(self) -> str:
        return self.language.subtag


class ExtLang(Subtag):
    """Extended language subtags are used to identify certain specially selected languages that, for various historical
    and compatibility reasons, are closely identified with or tagged using an existing primary language subtag.
    Extended language subtags are always used with their enclosing primary language subtag (indicated with a 'Prefix'
    field in the registry) when used to form the language tag. All languages that have an extended language subtag in
    the registry also have an identical primary language subtag record in the registry. This primary language subtag is
    RECOMMENDED for forming the language tag. The following rules apply to the extended language:

    1. Extended language subtags consist solely of three-letter subtags. All extended language subtag records defined
       in the registry were defined according to the assignments found in [ISO639-3]. Language collections and
       groupings, such as defined in [ISO639-5], are specifically excluded from being extended language subtags.
    2. Extended language subtag records MUST include exactly one 'Prefix' field indicating an appropriate subtag or
       sequence of subtags for that extended language subtag.
    3. Extended language subtag records MUST include a 'Preferred-Value'. The 'Preferred-Value' and 'Subtag' fields
       MUST be identical.
    4. Although the ABNF production 'extlang' permits up to three extended language tags in the language tag, extended
       language subtags MUST NOT include another extended language subtag in their 'Prefix'. That is, the second and
       third extended language subtag positions in a language tag are permanently reserved and tags that include those
       subtags in that position are, and will always remain, invalid.

    For example, the macrolanguage Chinese ('zh') encompasses a number of languages. For compatibility reasons, each of
    these languages has both a primary and extended language subtag in the registry. A few selected examples of these
    include Gan Chinese ('gan'), Cantonese Chinese ('yue'), and Mandarin Chinese ('cmn'). Each is encompassed by the
    macrolanguage 'zh' (Chinese).  Therefore, they each have the prefix "zh" in their registry records. Thus, Gan
    Chinese is represented with tags beginning "zh-gan" or "gan", Cantonese with tags beginning either "yue" or
    "zh-yue", and Mandarin Chinese with "zh-cmn" or "cmn".  The language subtag 'zh' can still be used without an
    extended language subtag to label a resource as some unspecified variety of Chinese, while the primary language
    subtag ('gan', 'yue', 'cmn') is preferred to using the extended language form ("zh-gan", "zh-yue", "zh-cmn").

    Extract from https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""
    preferred_value: ExtLangPreferredValue
    prefix: List[ExtLangPrefix]
    macro_language: Annotated[Optional[Language], MACRO_LANGUAGE_FIELD_INFO] = None
    deprecated: Annotated[Optional[datetime], DEPRECATED_FIELD_INFO] = None

    @field_validator('preferred_value')
    def preferred_value_subtag_validator(cls, value: Language, validation_info: ValidationInfo):
        if value.language.subtag != validation_info.data['subtag']:
            raise ValueError('Preferred_value must be equal than subtag. In the moment of writing this validation all'
                             'extension languages are languages, so, it is possible that this validation it is not '
                             'necessary any more.')
        return value

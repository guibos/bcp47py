"""Module that contains PreferredValue class."""

import abc
from abc import ABC
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

_TAG_FIELD_INFO = Field(examples=['en-GB-oxendict', 'jbo'])

class PreferredValue(BaseModel, ABC):
    """The field 'Preferred-Value' contains a mapping between the record in which it appears and another tag or subtag
    (depending on the record's 'Type').  The value in this field is used for canonicalization (see Section 4.5). In
    cases where the subtag or tag also has a 'Deprecated' field, then the 'Preferred-Value' is RECOMMENDED as the best
    choice to represent the value of this record when selecting a language tag.

    Records containing a 'Preferred-Value' fall into one of these four groups:

    1. ISO 639 language codes that were later withdrawn in favor of other codes.  These values are mostly a historical
       curiosity. The 'he'/'iw' pairing above is an example of this.
    2. Subtags (with types other than language or extlang) taken from codes or values that have been withdrawn in favor
       of a new code. In particular, this applies to region subtags taken from ISO 3166-1, because sometimes a country
       will change its name or administration in such a way that warrants a new region code. In some cases, countries
       have reverted to an older name, which might already be encoded. For example, the subtag 'ZR' (Zaire) was
       replaced by the subtag 'CD' (Democratic Republic of the Congo) when that country's name was changed.
    3. Tags or subtags that have become obsolete because the values they represent were later encoded. Many of the
       grandfathered or redundant tags were later encoded by ISO 639, for example, and fall into this grouping. For
       example, "i-klingon" was deprecated when the subtag 'tlh' was added.  The record for "i-klingon" has a
       'Preferred-Value' of 'tlh'.
    4. Extended language subtags always have a mapping to their identical primary language subtag. For example, the
       extended language subtag 'yue' (Cantonese) can be used to form the tag "zh-yue".  It has a 'Preferred-Value'
       mapping to the primary language subtag 'yue', meaning that a tag such as "zh-yue-Hant-HK" can be canonicalized
       to "yue-Hant-HK".

    Records other than those of type 'extlang' that contain a 'Preferred-Value' field MUST also have a 'Deprecated'
    field. This field contains the date on which the tag or subtag was deprecated in favorof the preferred value.

    For records of type 'extlang', the 'Preferred-Value' field appears without a corresponding 'Deprecated' field. An
    implementation MAY ignore these preferred value mappings, although if it ignores the mapping, it SHOULD do so
    consistently.  It SHOULD also treat the 'Preferred-Value' as equivalent to the mapped item.  For example, the tags
    "zh-yue-Hant-HK" and "yue-Hant-HK" are semantically equivalent and ought to be treated as if they were the same tag.

    Occasionally, the deprecated code is preferred in certain contexts. For example, both "iw" and "he" can be used in
    the Java programming language, but "he" is converted on input to "iw", which is thus the canonical form in Java.

    'Preferred-Value' mappings in records of type 'region' sometimes do not represent exactly the same meaning as the
    original value. There are many reasons for a country code to be changed, and the effect this has on the formation
    of language tags will depend on the nature of the change in question.  For example, the region subtag 'YD'
    (Democratic Yemen) was deprecated in favor of the subtag 'YE' (Yemen) when those two countries unified in 1990.

    A 'Preferred-Value' MAY be added to, changed, or removed from records according to the rules in Section 3.3.
    Addition, modification, or removal of a 'Preferred-Value' field in a record does not imply that content using the
    affected subtag needs to be retagged.

    The 'Preferred-Value' fields in records of type "grandfathered" and "redundant" each contain an "extended language
    range" [RFC4647] that is strongly RECOMMENDED for use in place of the record's value. In many cases, these mappings
    were created via deprecation of the tags during the period before [RFC4646] was adopted.  For example, the tag
    "no-nyn" was deprecated in favor of the ISO 639-1-defined language code 'nn'.

    The 'Preferred-Value' field in subtag records of type "extlang" also contains an "extended language range".
    This allows the subtag to be deprecated in favor of either a single primary language subtag or a new
    language-extlang sequence.

    Usually, the addition, removal, or change of a 'Preferred-Value' field for a subtag is done to reflect changes in
    one of the source standards.  For example, if an ISO 3166-1 region code is deprecated in favor of another code,
    that SHOULD result in the addition of a 'Preferred-Value' field.

    Extraction from https://www.rfc-editor.org/rfc/bcp/bcp47.txt

    Classes that inherits from this class must have attributes for each subtag that could be used."""

    model_config = ConfigDict(extra='forbid')

    @property
    @abc.abstractmethod
    def tag(self) -> Annotated[str, _TAG_FIELD_INFO]:
        """Returns preferred_value tag in string format. It will contain all subtags of the preferred value. Must
        return the same data that language-subtag-registry Preferred-Value field provides."""

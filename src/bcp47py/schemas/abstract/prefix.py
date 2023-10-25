import abc
from abc import ABC
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


_TAG_FIELD_INFO = Field(examples=['ar', 'zh-Latn'])


class Prefix(ABC, BaseModel):
    """The field 'Prefix' contains a valid language tag that is RECOMMENDED as one possible prefix to this record's
    subtag, perhaps with other subtags.  That is, when including an extended language or a variant subtag that has at
    least one 'Prefix' in a language tag, the resulting tag SHOULD match at least one of the subtag's 'Prefix' fields
    using the "Extended Filtering" algorithm (see [RFC4647]), and each of the subtags in that 'Prefix' SHOULD appear
    before the subtag itself.

    The 'Prefix' field MUST appear exactly once in a record of type 'extlang'. The 'Prefix' field MAY appear multiple
    times (or not at all) in records of type 'variant'.  Additional fields of this type MAY be added to a 'variant'
    record via the registration process, provided the 'variant' record already has at least one 'Prefix' field.

    Each 'Prefix' field indicates a particular sequence of subtags that form a meaningful tag with this subtag. For
    example, the extended language subtag 'cmn' (Mandarin Chinese) only makes sense with its prefix 'zh' (Chinese).
    Similarly, 'rozaj' (Resian, a dialect of Slovenian) would be appropriate when used with its prefix 'sl'
    (Slovenian), while tags such as "is-1994" are not appropriate (and probably not meaningful). Although the 'Prefix'
    for 'rozaj' is "sl", other subtags might appear between them.  For example, the tag "sl-IT-rozaj" (Slovenian,
    Italy, Resian) matches the 'Prefix' "sl".

    The 'Prefix' also indicates when variant subtags make sense when used together (many that otherwise share a
    'Prefix' are mutually exclusive) and what the relative ordering of variants is supposed to be. For example, the
    variant '1994' (Standardized Resian orthography) has several 'Prefix' fields in the registry ("sl-rozaj",
    "sl-rozaj-biske", "sl-rozaj-njiva", "sl-rozaj-osojs", and "sl-rozaj-solba").  This indicates not only that '1994'
    is appropriate to use with each of these five Resian variant subtags ('rozaj', 'biske', 'njiva', 'osojs', and
    'solba'), but also that it SHOULD appear following any of these variants in a tag. Thus, the language tag ought to
    take the form "sl-rozaj-biske-1994", rather than "sl-1994-rozaj-biske" or "sl-rozaj-1994-biske".

    Extraction from https://www.rfc-editor.org/rfc/bcp/bcp47.txt

    Classes that inherits from this class must have attributes for each subtag that could be used."""

    model_config = ConfigDict(extra='forbid')

    @property
    @abc.abstractmethod
    def tag(self) -> Annotated[str, _TAG_FIELD_INFO]:
        """Returns prefix tag in string format. It will contain all subtags of the prefix. Must
        return the same data that language-subtag-registry Prefix field provides."""
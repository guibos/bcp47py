from datetime import datetime

from pydantic import Field

DEPRECATED_FIELD_INFO = Field(
    title="deprecated",
    description="The field 'Deprecated' contains the date the record was deprecated and MAY be added, changed, or "
    "removed from any record via the maintenance process described in Section 3.3 or via the "
    "registration process described in Section 3.5.  Usually, the addition of a 'Deprecated' "
    "field is due to the action of one of the standards bodies, such as ISO 3166, withdrawing a code. "
    "Although valid in language tags, subtags and tags with a 'Deprecated' field are deprecated, and "
    "validating processors SHOULD NOT generate these subtags.  Note that a record that contains a "
    "'Deprecated' field and no corresponding 'Preferred-Value' field has no replacement mapping.\n"
    "In some historical cases, it might not have been possible to reconstruct the original deprecation "
    "date.  For these cases, an approximate date appears in the registry.  Some subtags and some "
    "grandfathered or redundant tags were deprecated before the initial creation of the registry. "
    "The exact rules for this appear in Section 2 of [RFC4645].  Note that these records have a "
    "'Deprecated' field with an earlier date then the corresponding 'Added' field!\n"
    "Extracted from ",
    examples=[datetime(2020, 1, 1)])

MACRO_LANGUAGE_FIELD_INFO = Field(title="macro_language", description="", examples=[])

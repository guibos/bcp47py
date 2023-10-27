from datetime import datetime

from pydantic import Field

from schemas.language import Language

DEPRECATED_FIELD_INFO = Field(
    title="deprecated",
    description="""The field 'Deprecated' contains the date the record was deprecated and MAY be added, changed, or 
    removed from any record via the maintenance process described in Section 3.3 or via the registration process 
    described in Section 3.5.  Usually, the addition of a 'Deprecated' field is due to the action of one of the 
    standards bodies, such as ISO 3166, withdrawing a code. Although valid in language tags, subtags and tags with a 
    'Deprecated' field are deprecated, and validating processors SHOULD NOT generate these subtags.  Note that a 
    record that contains a 'Deprecated' field and no corresponding 'Preferred-Value' field has no replacement mapping.
    
    In some historical cases, it might not have been possible to reconstruct the original deprecation date. For these 
    cases, an approximate date appears in the registry.  Some subtags and some grandfathered or redundant tags were 
    deprecated before the initial creation of the registry. The exact rules for this appear in Section 2 of [RFC4645]. 
    Note that these records have a 'Deprecated' field with an earlier date then the corresponding 'Added' field!
    
    Extract from https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[datetime(2020, 1, 1)])

MACRO_LANGUAGE_FIELD_INFO = Field(
    title="macro_language",
    description="""The field 'Macrolanguage' contains a primary language subtag (whose record appears in the registry). 
    This field indicates a language that encompasses this subtag's language according to assignments made by ISO 639-3.

    ISO 639-3 labels some languages in the registry as "macrolanguages". ISO 639-3 defines the term "macrolanguage" 
    to mean "clusters of closely-related language varieties that [...] can be considered distinct individual languages, 
    yet in certain usage contexts a single language identity for all is needed". These correspond to codes registered 
    in ISO 639-2 as individual languages that were found to correspond to more than one language in ISO 639-3.
    
    A language contained within a macrolanguage is called an "encompassed language".  The record for each encompassed 
    language contains a 'Macrolanguage' field in the registry; the macrolanguages themselves are not specially marked. 
    Note that some encompassed languages have ISO 639-1 or ISO 639-2 codes.
    
    The 'Macrolanguage' field can only occur in records of type 'language' or 'extlang'. Only values assigned by 
    ISO 639-3 will be considered for inclusion. 'Macrolanguage' fields MAY be added or removed via the normal 
    registration process whenever ISO 639-3 defines new values or withdraws old values. Macrolanguages are 
    informational, and MAY be removed or changed if ISO 639-3 changes the values. For more information on the use of 
    this field and choosing between macrolanguage and encompassed language subtags, see Section 4.1.1.
    
    For example, the language subtags 'nb' (Norwegian Bokmal) and 'nn' (Norwegian Nynorsk) each have a 'Macrolanguage' 
    field with a value of 'no' (Norwegian).  For more information, see Section 4.1.
    
    Extract from https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[
        Language(subtag='nb',
                 description=['Norwegian Bokmål'],
                 added=datetime(2005, 10, 16),
                 updated_at=datetime.today())
    ])

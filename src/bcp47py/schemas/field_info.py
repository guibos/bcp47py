"""Module that contains some information that could be used as annotation."""
from datetime import datetime

from pydantic import Field

DEPRECATED_FIELD_INFO = Field(
    title="deprecated",
    description="""The field 'Deprecated' contains the date the record was deprecated and MAY be added, changed, or 
    removed from any record via the maintenance process.
     
    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[datetime(2020, 1, 1)])

MACRO_LANGUAGE_FIELD_INFO = Field(
    title="macro_language",
    description="""The field 'Macrolanguage' contains a primary language subtag (whose record appears in the registry). 
    This field indicates a language that encompasses this subtag's language according to assignments made by ISO 639-3.

    For more information https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[
        # Language(subtag='nb',
        #          description=['Norwegian Bokmål'],
        #          added=datetime(2005, 10, 16),
        #          updated_at=datetime.today())
    ])

COMMENTS_FIELD_INFO = Field(
    title="comments",
    description="""The field 'Comments' contains additional information about the record and MAY appear more than once 
    per record. The field-body MAY include the full range of Unicode characters and is not restricted to any 
    particular script. This field MAY be inserted or changed via the registration process, and no guarantee of 
    stability is provided.
    
    For more information https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=[
        ["sr, hr, bs are preferred for most modern uses"],
        ["Non real example.", "Another non real example."]
    ]

)
TAG_FIELD_INFO = Field(examples=['en-GB-oxendict', 'jbo'])

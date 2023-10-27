"""Module that contains Subtag mixin class."""
from typing import Annotated

from pydantic import Field, ConfigDict

from schemas.mixin.base_type import BaseType

_SUBTAG_FIELD_INFO = Field(title="subtag",
                           description="""The field 'Subtag' contains the subtag defined in the record.
    
    The 'Subtag' field-body MUST follow the casing conventions described in Section 2.1.1. All subtags use lowercase 
    letters in the field-body, with two exceptions:
     - Subtags whose 'Type' field is 'script' (in other words, subtags defined by ISO 15924) MUSTuse titlecase.
     - Subtags whose 'Type' field is 'region' (in other words, the non-numeric region subtags defined  by ISO 3166-1) 
       MUST use all uppercase.
    
    Extract from https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
                           examples=["en", "aao", "Latn", "GB", "basiceng"])


class Subtag(BaseType):
    """Mixin that must be used by subtag types (all except redundant and grandfathered types)."""
    subtag: Annotated[str, _SUBTAG_FIELD_INFO]

"""Module that contains Subtag mixin class."""
from typing import Annotated

from pydantic import Field, ConfigDict

from schemas.mixin.base_type import BaseType

_SUBTAG_FIELD_INFO = Field(
    title="subtag",
    description="""The field 'Subtag' contains the subtag defined in the record.
    
    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
    examples=["en", "aao", "Latn", "GB", "basiceng"])


class Subtag(BaseType):
    """Mixin that must be used by subtag types (all except :class:schemas.redundant.Redundant and
    :class:schemas.grandfathered.Grandfathered types)."""
    subtag: Annotated[str, _SUBTAG_FIELD_INFO]

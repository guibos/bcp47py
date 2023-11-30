"""Module that contains Subtag abstract class."""
from typing import Annotated

from pydantic import Field

from schemas.mixin.base_type import BaseType

_SUBTAG_FIELD_INFO = Field(title="subtag",
                           description="""The field 'Subtag' contains the subtag defined in the record.
    
    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt""",
                           examples=["en", "aao", "Latn", "GB", "basiceng"])


class Subtag(BaseType):
    """Mixin that must be used by subtag types (all except :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.redundant.Redundant` and
    :class:`from exceptions.invalid.mixin.invalid_data_error import InvalidDataErrorschemas.grandfathered.Grandfathered` types)."""
    subtag: Annotated[str, _SUBTAG_FIELD_INFO]

    @property
    def tag_str(self) -> str:
        return self.subtag

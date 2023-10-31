"""Module that contains PreferredValue class."""

import abc
from abc import ABC
from typing import Annotated

from pydantic import BaseModel, ConfigDict

from schemas.field_info import TAG_FIELD_INFO


class PreferredValue(BaseModel, ABC):
    """The field 'Preferred-Value' contains a mapping between the record in which it appears and another tag or subtag
    depending on the record's 'Type'. In cases where the subtag or tag also has a
    :func:schemas.field_info.DEPRECATED_FIELD_INFO field, then the 'Preferred-Value' is RECOMMENDED as the best choice
    to represent the value of this record when selecting a language tag. Classes that inherits from this class must
    have attributes for each subtag that could be used.

    For more information check: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""

    model_config = ConfigDict(extra='forbid')

    @property
    @abc.abstractmethod
    def tag(self) -> Annotated[str, TAG_FIELD_INFO]:
        """Returns preferred_value tag in string format. It will contain all subtags of the preferred value. Must
        return the same data that language-subtag-registry Preferred-Value field provides."""

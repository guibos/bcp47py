import abc
from abc import ABC
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field

_TAG_FIELD_INFO = Field(examples=['ar', 'zh-Latn'])


class Prefix(ABC, BaseModel):
    """The field 'Prefix' contains a valid language tag that is RECOMMENDED as one possible prefix to this record's
    subtag, perhaps with other subtags. Classes that inherits from this class must have attributes for each subtag that
    could be used.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""

    model_config = ConfigDict(extra='forbid')

    @property
    @abc.abstractmethod
    def tag(self) -> Annotated[str, _TAG_FIELD_INFO]:
        """Returns prefix tag in string format. It will contain all subtags of the prefix. Must
        return the same data that language-subtag-registry Prefix field provides."""

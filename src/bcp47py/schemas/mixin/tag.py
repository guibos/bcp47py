from typing import Annotated

from pydantic import Field

from schemas.mixin.base_type import BaseType


class Tag(BaseType):
    """Mixin that must be used by tag types (only redundant and grandfathered types)."""
    tag: Annotated[str,
                   Field(title="tag",
                         description="The field 'Tag' appears in records whose 'Type' is either "
                         "'grandfathered' or 'redundant' and contains a tag registered under [RFC3066]",
                         examples=["art-lojban", "zh-yue"])]

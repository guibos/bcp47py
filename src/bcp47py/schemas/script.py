"""Module related with Script classes."""
from typing import Annotated, List

from schemas.field_info import COMMENTS_FIELD_INFO
from schemas.mixin.subtag import Subtag


class Script(Subtag):
    """Script subtags are used to indicate the script or writing system variations that distinguish the written forms
    of a language or its dialects.

    For more information: https://www.rfc-editor.org/rfc/bcp/bcp47.txt"""
    comments: Annotated[List[str], COMMENTS_FIELD_INFO] = []

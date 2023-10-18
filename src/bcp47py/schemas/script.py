from typing import Optional

from schemas.mixin.subtag import Subtag


class Script(Subtag):
    comments: Optional[str] = None

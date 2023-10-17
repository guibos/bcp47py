from typing import Optional

from schemas.abstract.subtag import Subtag


class Script(Subtag):
    comments: Optional[str] = None

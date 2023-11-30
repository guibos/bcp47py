"""Utility module that update language subtag registry."""
from typing import Annotated
from urllib.request import urlopen

from pydantic import Field

from mixin.base import Base

_FILE_CONTENT_FIELD_INFO = Field(
    title="File Content",
    description="""File content in string format.""",
    examples=[
        """File-Date: 2023-10-16
        %%
        Type: language
        Subtag: aa
        Description: Afar
        Added: 2005-10-16
        %%
        ...""",
    ]

)


class DownloaderService(Base):  # pylint: disable=too-few-public-methods
    """Utility class that update language subtag registry."""
    _LANGUAGE_SUBTAG_REGISTRY_URL = 'https://www.iana.org/assignments/language-subtag-registry/language-subtag-registry'

    def download(self):
        """Method that update language subtag registry."""
        with open(self._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH, 'w', encoding=self._LANGUAGE_SUBTAG_REGISTRY_ENCODING) as f:
            f.write(self._get_data())

    def _get_data(self) -> Annotated[str, _FILE_CONTENT_FIELD_INFO]:
        with urlopen(self._LANGUAGE_SUBTAG_REGISTRY_URL) as response:
            data = response.read().decode('utf-8')

        if not data:
            raise RuntimeError("Problems to download BCP47 data.")
        return data


if __name__ == '__main__':
    DownloaderService().download()

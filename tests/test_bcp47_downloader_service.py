import pytest

from src.bcp47py.bcp47_downloader_service import BCP47DownloaderService


@pytest.mark.download
def test_bcp47_downloader_service(tmp_path):
    tmp_file = tmp_path / "language-subtag-registry"

    class BCP47DownloaderServiceMock(BCP47DownloaderService):
        _LANGUAGE_SUBTAG_REGISTRY_FILE_PATH = tmp_file

    BCP47DownloaderServiceMock().download()

    with open(tmp_file, 'r') as f:
        assert f.read()

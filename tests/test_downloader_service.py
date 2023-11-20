import filecmp
from pathlib import Path

import pytest
from _pytest.fixtures import fixture
from _pytest.tmpdir import TempPathFactory

from mixin.base import Base
from downloader_service import DownloaderService


@fixture(scope='session')
def last_data_path(tmp_path_factory: TempPathFactory) -> Path:
    tmp_file = tmp_path_factory.mktemp("data") / "language-subtag-registry"

    class BCP47DownloaderServiceMock(DownloaderService):
        _LANGUAGE_SUBTAG_REGISTRY_FILE_PATH = tmp_file

    BCP47DownloaderServiceMock().download()
    return tmp_file


@pytest.mark.download
def test_downloader_service(last_data_path: Path):
    with open(last_data_path, 'r', encoding='utf-8') as f:
        assert f.read()


@pytest.mark.download
def test_downloader_service_check_last_data(last_data_path: Path):
    project_data = Base._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH

    assert filecmp.cmp(last_data_path, project_data)

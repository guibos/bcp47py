import os

import pytest

from interface.bcp47_repository.bcp47_repository_interface import BCP47RepositoryInterface
from repository import Repository


@pytest.fixture(scope="session")
def mocked_data_path() -> str:
    return os.path.join(os.path.dirname(__file__), 'fixtures', 'language-subtag-registry')


@pytest.fixture(scope="session")
def repository(mocked_data_path: str) -> BCP47RepositoryInterface:
    return Repository(mocked_data_path)

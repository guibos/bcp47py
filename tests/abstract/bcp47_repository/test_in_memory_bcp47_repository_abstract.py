import pytest

from enums.language_scope import LanguageScopeEnum
from interface.bcp47_repository.bcp47_repository_interface import BCP47RepositoryInterface
from repository import Repository
from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.variant import Variant

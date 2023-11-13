import pytest

from interface.repository_interface import RepositoryInterface
from enums.language_scope import LanguageScopeEnum
from repository import Repository
from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.variant import Variant


@pytest.fixture(scope="session")
def repository() -> RepositoryInterface:
    return Repository()


def test_bcp_data_script(repository: RepositoryInterface):
    assert repository.scripts

    for script in repository.scripts:
        assert isinstance(script, Script)

    latin = repository.get_script_by_subtag('Latn')
    assert latin.description == ['Latin']


def test_bcp47_data_languages(repository: RepositoryInterface):
    assert repository.languages

    for language in repository.languages:
        assert isinstance(language, Language)

    english = repository.get_language_by_subtag('en')
    assert english.description == ['English']


def test_bcp47_data_language_scope(repository: RepositoryInterface):
    assert len(repository.languages_scopes) == len(LanguageScopeEnum)

    for language_scope in repository.languages_scopes:
        assert isinstance(language_scope, LanguageScope)

    for language_scope in LanguageScopeEnum:
        assert repository.get_language_scope_by_name(language_scope.value).scope == language_scope


def test_bcp47_data_ext_lang(repository: RepositoryInterface):
    assert repository.ext_langs

    for ext_lang in repository.ext_langs:
        assert isinstance(ext_lang, ExtLang)

    algerian_saharan_arabic = repository.get_ext_lang_by_subtag('aao')
    assert algerian_saharan_arabic.description == ['Algerian Saharan Arabic']


def test_bcp47_data_region(repository: RepositoryInterface):
    assert repository.regions

    for region in repository.regions:
        assert isinstance(region, Region)

    spain = repository.get_region_by_subtag('es')
    assert spain.description == ['Spain']


def test_bcp47_data_variant(repository: RepositoryInterface):
    assert repository.variants

    for variant in repository.variants:
        assert isinstance(variant, Variant)

    valencia = repository.get_variant_by_subtag('valencia')
    assert valencia.description == ['Valencian']


def test_bcp47_data_grandfathered(repository: RepositoryInterface):
    assert repository.grandfathered

    for grandfathered in repository.grandfathered:
        assert isinstance(grandfathered, Grandfathered)

    gaulish = repository.get_grandfathered_by_tag('cel-gaulish')
    assert gaulish.description == ['Gaulish']


def test_bcp47_data_redundant(repository: RepositoryInterface):
    assert repository.redundant

    for redundant in repository.redundant:
        assert isinstance(redundant, Redundant)

    german_traditional = repository.get_redundant_by_tag('de-1901')
    assert german_traditional.description == ['German, traditional orthography']

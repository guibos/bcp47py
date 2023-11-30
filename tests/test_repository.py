import dataclasses
import datetime
from typing import List, Union, Type

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
from type_aliases import TagsOrSubtagType, MainDataObjects


@dataclasses.dataclass
class CheckTypeRelationship:
    data_list: List[MainDataObjects]
    schema: Type


def _check_type(data_list: List[MainDataObjects], schema: Type):
    for data_object in data_list:
        isinstance(data_object, schema)


def _generic_test_repo(repository: BCP47RepositoryInterface):
    relationships = [
        CheckTypeRelationship(repository.scripts, Script),
        CheckTypeRelationship(repository.languages_scopes, LanguageScope),
        CheckTypeRelationship(repository.languages, Language),
        CheckTypeRelationship(repository.ext_langs, ExtLang),
        CheckTypeRelationship(repository.regions, Region),
        CheckTypeRelationship(repository.variants, Variant),
        CheckTypeRelationship(repository.grandfathered, Grandfathered),
        CheckTypeRelationship(repository.redundant, Redundant)
    ]
    for relationship in relationships:
        _check_type(relationship.data_list, relationship.schema)


def test_generic_repository_non_mocked_data():
    repository = Repository()
    _generic_test_repo(repository)


def test_generic_repository_mocked_data(repository: BCP47RepositoryInterface):
    _generic_test_repo(repository)


def test_script_latin(repository: BCP47RepositoryInterface):
    script = repository.get_script_by_subtag('Latn')
    assert script.subtag == 'Latn'
    assert script.description == ['Latin']
    assert script.comments == []
    assert script.added == datetime.datetime(2005, 10, 16)
    assert script.updated_at == datetime.datetime(2023, 10, 16)


def test_script_fake(repository: BCP47RepositoryInterface):
    script = repository.get_script_by_subtag('Fake')
    assert script.subtag == 'Fake'
    assert script.description == ['Fake script', 'Another Fake Script']
    assert script.comments == ['Fake comment for a fake script', 'Another fake comment']
    assert script.added == datetime.datetime(2011, 1, 7)
    assert script.updated_at == datetime.datetime(2023, 10, 16)


def test_language_english(repository: BCP47RepositoryInterface):
    language = repository.get_language_by_subtag('en')
    assert language.added == datetime.datetime(2005, 10, 16)
    assert language.comments == []
    assert language.deprecated is None
    assert language.description == ['English']
    assert language.macro_language
    assert langu


    for language in repository.languages:
        assert isinstance(language, Language)

    english = repository.get_language_by_subtag('en')
    assert english.description == ['English']
#
#
# def test_bcp47_data_language_scope(repository: BCP47RepositoryInterface):
#     assert len(repository.languages_scopes) == len(LanguageScopeEnum)
#
#     for language_scope in repository.languages_scopes:
#         assert isinstance(language_scope, LanguageScope)
#
#     for language_scope in LanguageScopeEnum:
#         assert repository.get_language_scope_by_name(language_scope.value).scope == language_scope
#
#
# def test_bcp47_data_ext_lang(repository: BCP47RepositoryInterface):
#
#     assert repository.ext_langs
#
#     for ext_lang in repository.ext_langs:
#         assert isinstance(ext_lang, ExtLang)
#
#     algerian_saharan_arabic = repository.get_ext_lang_by_subtag('aao')
#     assert algerian_saharan_arabic.description == ['Algerian Saharan Arabic']
#
#
# def test_bcp47_data_region(repository: BCP47RepositoryInterface):
#     assert repository.regions
#
#     for region in repository.regions:
#         assert isinstance(region, Region)
#
#     spain = repository.get_region_by_subtag('es')
#     assert spain.description == ['Spain']
#
#
# def test_bcp47_data_variant(repository: BCP47RepositoryInterface):
#     assert repository.variants
#
#     for variant in repository.variants:
#         assert isinstance(variant, Variant)
#
#     valencia = repository.get_variant_by_subtag('valencia')
#     assert valencia.description == ['Valencian']
#
#
# def test_bcp47_data_grandfathered(repository: BCP47RepositoryInterface):
#     assert repository.grandfathered
#
#     for grandfathered in repository.grandfathered:
#         assert isinstance(grandfathered, Grandfathered)
#
#     gaulish = repository.get_grandfathered_by_tag('cel-gaulish')
#     assert gaulish.description == ['Gaulish']
#
#
# def test_bcp47_data_redundant(repository: BCP47RepositoryInterface):
#     assert repository.redundant
#
#     for redundant in repository.redundant:
#         assert isinstance(redundant, Redundant)
#
#     german_traditional = repository.get_redundant_by_tag('de-1901')
#     assert german_traditional.description == ['German, traditional orthography']
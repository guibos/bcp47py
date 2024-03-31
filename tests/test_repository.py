import dataclasses
import datetime
from typing import List, Type, Iterable

from enums.language_scope import LanguageScopeEnum
from interface.bcp47_repository.bcp47_repository_interface import BCP47RepositoryInterface
from repository import Repository
from schemas.ext_lang import ExtLang, ExtLangPrefix, ExtLangPreferredValue
from schemas.grandfathered import Grandfathered
from schemas.language import Language, LanguagePreferredValue
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant, RedundantPreferredValue
from schemas.region import Region, RegionPreferredValue
from schemas.script import Script
from schemas.variant import Variant, VariantPrefix, VariantPreferredValue
from type_aliases import TagsOrSubtagType, MainDataObjects


@dataclasses.dataclass
class CheckTypeRelationship:
    data_list: Iterable[MainDataObjects]
    schema: Type


def _check_type(data_list: Iterable[MainDataObjects], schema: Type):
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


def test_generic_non_mocked_data():
    repository = Repository()
    _generic_test_repo(repository)


def test_generic_mocked_data(repository: BCP47RepositoryInterface):
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
    assert language.description == ['English']
    assert language.added == datetime.datetime(2005, 10, 16)
    assert language.updated_at == datetime.datetime(2023, 10, 16)
    assert language.subtag == 'en'
    assert language.macro_language is None
    assert language.scope is None
    assert language.comments == []
    assert language.suppress_script == repository.get_script_by_subtag('Latn')
    assert language.preferred_value is None
    assert language.deprecated is None


def test_language_austro_asiatic(repository: BCP47RepositoryInterface):
    language = repository.get_language_by_subtag('aav')
    assert language.description == ['Austro-Asiatic languages']
    assert language.added == datetime.datetime(2009, 7, 29)
    assert language.updated_at == datetime.datetime(2023, 10, 16)
    assert language.subtag == 'aav'
    assert language.macro_language is None
    assert language.scope == repository.get_language_scope_by_name('macrolanguage')
    assert language.comments == []
    assert language.suppress_script == repository.get_script_by_subtag('Latn')
    assert language.preferred_value is None
    assert language.deprecated is None


def test_language_fake(repository: BCP47RepositoryInterface):
    language = repository.get_language_by_subtag('f1')
    assert language.description == ['Fake Language', 'Fake Language F1']
    assert language.added == datetime.datetime(2005, 10, 16)
    assert language.updated_at == datetime.datetime(2023, 10, 16)
    assert language.subtag == 'f1'
    assert language.macro_language == repository.get_language_by_subtag('aav')
    assert language.scope is None
    assert language.comments == ['Fake language comment', 'Another language']
    assert language.suppress_script is None
    assert language.preferred_value == LanguagePreferredValue(language=repository.get_language_by_subtag('en'))
    assert language.preferred_value.tag == 'en'
    assert language.deprecated == datetime.datetime(2023, 8, 2)


def test_bcp47_data_language_scope(repository: BCP47RepositoryInterface):
    assert len(list(repository.languages_scopes)) == len(LanguageScopeEnum)

    for language_scope in repository.languages_scopes:
        assert isinstance(language_scope, LanguageScope)

    for language_scope in LanguageScopeEnum:
        assert repository.get_language_scope_by_name(language_scope.value).scope == language_scope


def test_bcp47_data_ext_lang_f1(repository: BCP47RepositoryInterface):
    ext_lang = repository.get_ext_lang_by_subtag('f1')

    assert ext_lang.description == ['Ext lang 2', '2']
    assert ext_lang.added == datetime.datetime(2020, 7, 29, 0, 0)
    assert ext_lang.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert ext_lang.subtag == 'f1'
    assert ext_lang.preferred_value == ExtLangPreferredValue(language=repository.get_language_by_subtag('f1'))
    assert ext_lang.preferred_value.tag == 'f1'
    assert ext_lang.prefix == [
        ExtLangPrefix(language=repository.get_language_by_subtag('f1')),
        ExtLangPrefix(language=repository.get_language_by_subtag('aav')),
    ]
    assert ext_lang.prefix[0].tag == 'f1'
    assert ext_lang.macro_language == repository.get_language_by_subtag('aav')
    assert ext_lang.deprecated == datetime.datetime(2010, 7, 29, 0, 0)


def test_bcp47_data_ext_lang_en(repository: BCP47RepositoryInterface):
    ext_lang = repository.get_ext_lang_by_subtag('en')

    assert ext_lang.description == ['Ext lang 1']
    assert ext_lang.added == datetime.datetime(2009, 7, 29, 0, 0)
    assert ext_lang.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert ext_lang.subtag == 'en'
    assert ext_lang.preferred_value == ExtLangPreferredValue(language=repository.get_language_by_subtag('en'))
    assert ext_lang.preferred_value.tag == 'en'
    assert ext_lang.prefix == [
        ExtLangPrefix(language=repository.get_language_by_subtag('f1')),
    ]
    assert ext_lang.prefix[0].tag == 'f1'
    assert ext_lang.macro_language is None
    assert ext_lang.deprecated is None


def test_bcp47_data_region_fk(repository: BCP47RepositoryInterface):
    region = repository.get_region_by_subtag('FK')

    assert region.description == ['Fake 1', 'Fake Plus']
    assert region.added == datetime.datetime(2005, 10, 16, 0, 0)
    assert region.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert region.subtag == 'FK'
    assert region.comments == []
    assert region.preferred_value == RegionPreferredValue(region=repository.get_region_by_subtag('GB'))
    assert region.preferred_value.tag() == 'GB'
    assert region.deprecated == datetime.datetime(2010, 7, 29, 0, 0)


def test_bcp47_data_region_gb(repository: BCP47RepositoryInterface):
    region = repository.get_region_by_subtag('GB')

    assert region.description == ['United Kingdom']
    assert region.added == datetime.datetime(2005, 10, 16, 0, 0)
    assert region.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert region.subtag == 'GB'
    assert region.comments == [
        'as of 2006-03-29 GB no longer includes the Channel Islands and Isle of Man; see GG, JE, IM'
    ]
    assert region.preferred_value is None
    assert region.deprecated is None


def test_bcp47_data_variant_fk(repository: BCP47RepositoryInterface):
    variant = repository.get_variant_by_subtag('fake1')
    assert variant.description == ['Variant test 1', 'Variant test 2'] != ['Valencian']
    assert variant.added == datetime.datetime(2005, 4, 17, 0, 0)
    assert variant.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert variant.subtag == 'fake1'
    assert variant.prefix == []
    assert variant.comments == []
    assert variant.preferred_value is None
    assert variant.deprecated is None


def test_bcp47_data_variant_oxendict(repository: BCP47RepositoryInterface):
    variant = repository.get_variant_by_subtag('oxendict')
    assert variant.description == ['Oxford English Dictionary spelling']
    assert variant.added == datetime.datetime(2005, 4, 17, 0, 0)
    assert variant.updated_at == datetime.datetime(2023, 10, 16, 0, 0)
    assert variant.subtag == 'oxendict'
    assert variant.prefix == [
        VariantPrefix(
            language=repository.get_language_by_subtag('en'),
            extlang=[repository.get_ext_lang_by_subtag('en'),
                     repository.get_ext_lang_by_subtag('f1')],  # FIXME:
            region=repository.get_region_by_subtag('GB'),
            script=repository.get_script_by_subtag('Latn'),
            variant=[repository.get_variant_by_subtag('fake1')]),
        VariantPrefix(language=repository.get_language_by_subtag('aav'),
                      extlang=[repository.get_ext_lang_by_subtag('f1')],
                      region=repository.get_region_by_subtag('FK'),
                      script=repository.get_script_by_subtag('Fake'),
                      variant=[repository.get_variant_by_subtag('fake1')]),
    ]
    assert variant.prefix[0].tag == 'en-en-f1-Latn-GB-fake1'
    assert variant.comments == ['test variant']
    assert variant.deprecated == datetime.datetime(2010, 7, 29, 0, 0)
    assert variant.preferred_value == VariantPreferredValue(variant=[repository.get_variant_by_subtag('fake1')])
    assert variant.preferred_value.tag == 'fake1'


def test_bcp47_data_redundant(repository: BCP47RepositoryInterface):
    redundant = repository.get_redundant_by_tag('f1')
    assert redundant.added == datetime.datetime(1999, 12, 18, 0, 0)
    assert redundant.deprecated == datetime.datetime(2009, 7, 29, 0, 0)
    assert redundant.description == ['English Latin']
    assert redundant.preferred_value == RedundantPreferredValue(language=repository.get_language_by_subtag('en'), )
    assert redundant.tag == 'f1'
    assert redundant.updated_at == datetime.datetime(2023, 10, 16, 0, 0)


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

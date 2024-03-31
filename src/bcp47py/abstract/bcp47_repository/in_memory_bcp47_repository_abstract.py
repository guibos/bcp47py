"""Module related with InMemoryBCP47RepositoryAbstract class."""
import abc
import dataclasses
from abc import ABC
from typing import List, Dict, Union, Callable, Any

from enums.bcp47_type import BCP47Type
from enums.language_scope import LanguageScopeEnum
from exceptions.not_found.ext_lang_subtag_not_found_error import ExtLangSubtagNotFoundError
from exceptions.not_found.grandfathered_tag_not_found_error import GrandfatheredTagNotFoundError
from exceptions.not_found.language_scope_not_found_error import LanguageScopeNotFoundError
from exceptions.not_found.language_subtag_not_found_error import LanguageSubtagNotFoundError
from exceptions.not_found.redundant_tag_not_found_error import RedundantTagNotFoundError
from exceptions.not_found.region_subtag_not_found_error import RegionSubtagNotFoundError
from exceptions.not_found.script_subtag_not_found_error import ScriptSubtagNotFoundError
from exceptions.not_found.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError
from exceptions.not_found.variant_subtag_not_found_error import VariantSubtagNotFoundError
from interface.bcp47_repository.bcp47_repository_interface import BCP47RepositoryInterface
from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.parsed_tag import ParsedTag
from schemas.variant import Variant
from type_aliases import TagsOrSubtagType, SubtagType

_TagParsedData = Dict[str, Union[SubtagType, List[SubtagType]]]


class InMemoryBCP47RepositoryAbstract(BCP47RepositoryInterface, ABC):
    """Basic in memory implementation of
    :class:`interface.bcp47_repository.bcp47_repository_interface.BCP47RepositoryInterface`. It requires implementation
    of :func:`abstract.bcp47_repository.in_memory_repository_abstract.InMemoryRepositoryAbstract._load_data` to work."""

    def __init__(self):
        self._languages: List[Language] = []
        self._languages_scopes: List[LanguageScope] = []
        self._ext_langs: List[ExtLang] = []
        self._scripts: List[Script] = []
        self._regions: List[Region] = []
        self._variants: List[Variant] = []
        self._grandfathered: List[Grandfathered] = []
        self._redundant: List[Redundant] = []

        self._SUBTAG_DATA_FINDER = [
            _SubtagDataFinder(self.get_language_by_subtag, BCP47Type.LANGUAGE, 1),
            _SubtagDataFinder(self.get_ext_lang_by_subtag, BCP47Type.EXTLANG, 3),
            _SubtagDataFinder(self.get_script_by_subtag, BCP47Type.SCRIPT, 1),
            _SubtagDataFinder(self.get_region_by_subtag, BCP47Type.REGION, 1),
            _SubtagDataFinder(self.get_variant_by_subtag, BCP47Type.VARIANT, 999)
        ]
        self._load_data()

    @property
    def languages(self) -> List[Language]:
        return self._languages

    def get_language_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Language:
        try:
            return self._subtag_filter(subtag, self.languages, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise LanguageSubtagNotFoundError(subtag) from e

    @property
    def languages_scopes(self) -> List[LanguageScope]:
        return self._languages_scopes

    def get_language_scope_by_name(self, name: str) -> LanguageScope:
        try:
            langauge_scope_enum = LanguageScopeEnum(name)
        except ValueError as e:
            raise LanguageScopeNotFoundError(name) from e

        for bcp47_language_scope in self.languages_scopes:
            if langauge_scope_enum == bcp47_language_scope.scope:
                return bcp47_language_scope
        raise RuntimeError(f'Unexpected workflow error to find a language scope: "{name}"')

    @property
    def ext_langs(self) -> List[ExtLang]:
        return self._ext_langs

    def get_ext_lang_by_subtag(self, subtag: str, case_sensitive: bool = False) -> ExtLang:
        try:
            return self._subtag_filter(subtag, self.ext_langs, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ExtLangSubtagNotFoundError(subtag) from e

    @property
    def scripts(self) -> List[Script]:
        return self._scripts

    def get_script_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Script:
        try:
            return self._subtag_filter(subtag, self.scripts, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ScriptSubtagNotFoundError(subtag) from e

    @property
    def regions(self) -> List[Region]:
        return self._regions

    def get_region_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Region:
        try:
            return self._subtag_filter(subtag, self.regions, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RegionSubtagNotFoundError(subtag) from e

    @property
    def variants(self) -> List[Variant]:
        return self._variants

    def get_variant_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Variant:
        try:
            return self._subtag_filter(subtag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise VariantSubtagNotFoundError(subtag) from e

    @property
    def grandfathered(self) -> List[Grandfathered]:
        return self._grandfathered

    def get_grandfathered_by_tag(self, tag: str, case_sensitive: bool = False) -> Grandfathered:
        try:
            return self._subtag_filter(tag, self.grandfathered, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise GrandfatheredTagNotFoundError(tag) from e

    @property
    def redundant(self) -> List[Redundant]:
        return self._redundant

    def get_redundant_by_tag(self, tag: str, case_sensitive: bool = False) -> Redundant:
        try:
            return self._subtag_filter(tag, self.redundant, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RedundantTagNotFoundError(tag) from e

    def tag_parser(self, tag: str, case_sensitive: bool = False) -> ParsedTag:
        """Method that parse a bcp47 string tag and return a dataclass with all subtags information."""
        return ParsedTag(**self._tag_parser(tag, case_sensitive))

    @staticmethod
    def _subtag_filter(subtag_str: str, tag_or_subtag_list: List[TagsOrSubtagType],
                       case_sensitive: bool) -> TagsOrSubtagType:
        """Method that helps to find a subtag object in a list through subtag string."""
        if not case_sensitive:
            subtag_str = subtag_str.lower()
        for subtag in tag_or_subtag_list:
            tag_str = subtag.tag_str
            if not case_sensitive:
                tag_str = tag_str.lower()
            if subtag_str == tag_str:
                return subtag
        raise TagOrSubtagNotFoundError(subtag_str)

    def _tag_parser(
            self, tag: str,
            case_sensitive: bool) -> Dict[str, Union[Language, ExtLang, Script, Region, Variant, ExtLang, Redundant]]:
        """Method that parse a string tag and return a Dict with all subtag objects contained in previous string tag.
        :raise exceptions.not_found.tag_or_subtag_not_found_error.TagOrSubtagNotFoundError:
        """
        tag_parsed_data = {}
        try:
            redundant = self.get_redundant_by_tag(tag)
            tag_parsed_data[BCP47Type.REDUNDANT.value] = redundant
        except RedundantTagNotFoundError:
            pass

        iterator = _SubtagDataFinderIterator(self._SUBTAG_DATA_FINDER)
        for subtag in tag.split('-'):
            found = False
            while found is False:
                try:
                    subtag_data_finder = iterator.next()
                except StopIteration:
                    raise TagOrSubtagNotFoundError(f"Subtag {subtag} of {tag} is not found.")
                try:
                    value = subtag_data_finder.callable(subtag, case_sensitive)
                except TagOrSubtagNotFoundError:
                    try:
                        iterator.next_subtag_type()
                    except StopIteration:
                        raise TagOrSubtagNotFoundError(f"Subtag {subtag} of {tag} is not found.")
                    continue

                if subtag_data_finder.max_subtags == 1:
                    tag_parsed_data[subtag_data_finder.bcp47_subtag_type.value] = value
                else:
                    try:
                        tag_parsed_data[subtag_data_finder.bcp47_subtag_type.value].append(value)
                    except KeyError:
                        tag_parsed_data[subtag_data_finder.bcp47_subtag_type.value] = [value]
                found = True
        return tag_parsed_data

    @abc.abstractmethod
    def _load_data(self):
        """Main function that is responsible to load all data in the instance."""


@dataclasses.dataclass
class _SubtagDataFinder:
    """Dataclass that have the relationship between bcp47 subtag type and the method that should be called to search
    the subtag. _SUBTAG_DATA_FINDER constant is a list that contains instances of this class that are used search in
    a specific order to parse a bcp47 tag."""
    callable: Callable[[str, bool], Any]
    bcp47_subtag_type: BCP47Type
    max_subtags: int

    def add_subtag_to_tag_parsed_data(self, tag_parsed_data: _TagParsedData, value: SubtagType) -> _TagParsedData:
        if self.max_subtags == 1:
            tag_parsed_data['bcp47_subtag_type'] = value
        else:
            try:
                tag_parsed_data['bcp47_subtag_type'].append(value)
            except KeyError:
                tag_parsed_data['bcp47_subtag_type'] = [value]
        return tag_parsed_data


class _SubtagDataFinderIterator:

    def __init__(self, subtag_data_finder: List[_SubtagDataFinder]):
        self._subtag_data_finder = subtag_data_finder
        self._list_iteration = 0
        self._subtag_repetition = -1

    def next(self) -> _SubtagDataFinder:
        self._subtag_repetition += 1
        if self._subtag_data_finder[self._list_iteration].max_subtags <= self._subtag_repetition:
            return self._next_subtag_finder()
        return self._subtag_data_finder[self._list_iteration]

    def _next_subtag_finder(self) -> _SubtagDataFinder:
        self.next_subtag_type()
        return self.next()

    def next_subtag_type(self):
        self._subtag_repetition = -1
        self._list_iteration += 1
        if len(self._subtag_data_finder) <= self._list_iteration:
            raise StopIteration

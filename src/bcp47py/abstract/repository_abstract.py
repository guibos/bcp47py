import abc
import dataclasses
from typing import List, Iterable, Dict, Union, Callable, Any

from enums.bcp47_type import BCP47Type
from enums.language_scope import LanguageScopeEnum
from exceptions.ext_lang_subtag_not_found_error import ExtLangSubtagNotFoundError
from exceptions.grandfathered_tag_not_found_error import GrandfatheredTagNotFoundError
from exceptions.language_scope_not_found_error import LanguageScopeNotFoundError
from exceptions.language_subtag_not_found_error import LanguageSubtagNotFoundError
from exceptions.redundant_tag_not_found_error import RedundantTagNotFoundError
from exceptions.region_subtag_not_found_error import RegionSubtagNotFoundError
from exceptions.script_subtag_not_found_error import ScriptSubtagNotFoundError
from exceptions.tag_or_subtag_not_found_error import TagOrSubtagNotFoundError
from exceptions.variant_subtag_not_found_error import VariantSubtagNotFoundError
from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.subtags import Subtags
from schemas.variant import Variant
from type_aliases import TagsOrSubtagType


@dataclasses.dataclass
class SubtagDataFinder:
    callable: Callable[[str, bool], Any]
    data_dict_key: BCP47Type


class RepositoryAbstract(abc.ABC):

    def __init__(self):
        self._SUBTAG_DATA_FINDER = [
            SubtagDataFinder(self.get_language_by_subtag, BCP47Type.LANGUAGE),
            SubtagDataFinder(self.get_ext_lang_by_subtag, BCP47Type.EXTLANG),
            SubtagDataFinder(self.get_script_by_subtag, BCP47Type.SCRIPT),
            SubtagDataFinder(self.get_region_by_subtag, BCP47Type.REGION),
            SubtagDataFinder(self.get_variant_by_subtag, BCP47Type.VARIANT)
        ]

    def tag_or_subtag_parser(self, tag_or_subtag: str, case_sensitive: bool = False) -> Subtags:
        return Subtags(**self._tag_or_subtag_parser(tag_or_subtag, case_sensitive))

    @property
    @abc.abstractmethod
    def languages(self) -> List[Language]:
        pass

    def get_language_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Language:
        try:
            return self._tag_or_subtag_filter(subtag, self.languages, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise LanguageSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def languages_scopes(self) -> List[LanguageScope]:
        pass

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
    @abc.abstractmethod
    def ext_langs(self) -> List[ExtLang]:
        pass

    def get_ext_lang_by_subtag(self, subtag: str, case_sensitive: bool = False) -> ExtLang:
        try:
            return self._tag_or_subtag_filter(subtag, self.ext_langs, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ExtLangSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def scripts(self) -> List[Script]:
        pass

    def get_script_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Script:
        try:
            return self._tag_or_subtag_filter(subtag, self.scripts, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ScriptSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def regions(self) -> List[Region]:
        pass

    def get_region_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Region:
        try:
            return self._tag_or_subtag_filter(subtag, self.regions, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RegionSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def variants(self) -> List[Variant]:
        pass

    def get_variant_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Variant:
        try:
            return self._tag_or_subtag_filter(subtag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise VariantSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def grandfathered(self) -> List[Grandfathered]:
        pass

    def get_grandfathered_by_tag(self, tag: str, case_sensitive: bool = False) -> Grandfathered:
        try:
            return self._tag_or_subtag_filter(tag, self.grandfathered, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise GrandfatheredTagNotFoundError(tag) from e

    @property
    @abc.abstractmethod
    def redundant(self) -> List[Redundant]:
        pass

    def get_redundant_by_tag(self, tag: str, case_sensitive: bool = False) -> Redundant:
        try:
            return self._tag_or_subtag_filter(tag, self.redundant, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RedundantTagNotFoundError(tag) from e

    def _tag_or_subtag_filter(self, subtag_str: str, tag_or_subtag_list: List[TagsOrSubtagType],
                              case_sensitive: bool) -> TagsOrSubtagType:
        if not case_sensitive:
            subtag_str = subtag_str.lower()
        for subtag in tag_or_subtag_list:
            tag_or_subtag_str = self._get_tag_or_subtag(subtag)
            if not case_sensitive:
                tag_or_subtag_str = tag_or_subtag_str.lower()
            if subtag_str == tag_or_subtag_str:
                return subtag
        raise TagOrSubtagNotFoundError(subtag_str)

    def _tag_or_subtag_parser(
            self, tag_or_subtag: str,
            case_sensitive: bool) -> Dict[str, Union[Language, ExtLang, Script, Region, Variant, ExtLang]]:
        i = 0
        tag_or_subtag_data = {}
        for subtag in tag_or_subtag.split('-'):
            while True:
                if i >= len(self._SUBTAG_DATA_FINDER):
                    raise TagOrSubtagNotFoundError(f"Subtag {subtag} of {tag_or_subtag} is not found.")
                try:
                    tag_or_subtag_data[
                        self._SUBTAG_DATA_FINDER[i].data_dict_key.value] = self._SUBTAG_DATA_FINDER[i].callable(
                            subtag, case_sensitive)
                    break
                except TagOrSubtagNotFoundError:
                    i += 1
                    continue
        return tag_or_subtag_data

    @staticmethod
    def _get_tag_or_subtag(model: TagsOrSubtagType) -> str:
        if str_tag_or_subtag := getattr(model, 'subtag', ''):
            return str_tag_or_subtag
        elif str_tag_or_subtag := getattr(model, 'tag', ''):
            return str_tag_or_subtag
        raise RuntimeError("Tag or subtag not found.")

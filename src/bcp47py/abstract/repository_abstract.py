import abc
import dataclasses
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

    def tag_parser(self, tag: str, case_sensitive: bool = False) -> Subtags:
        """Parse string tag to get all subtags."""
        return Subtags(**self._tag_parser(tag, case_sensitive))

    @property
    @abc.abstractmethod
    def languages(self) -> List[Language]:
        """Return the list of :class:`schemas.language.Language` that are included in BCP47."""

    def get_language_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Language:
        """Return a class:`schemas.language.Language` by his subtag.

        :raise exceptions.not_found.language_subtag_not_found_error.LanguageSubtagNotFoundError:"""
        try:
            return self._tag_or_subtag_filter(subtag, self.languages, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise LanguageSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def languages_scopes(self) -> List[LanguageScope]:
        """Return the list of LanguagesScopes that are included in BCP47."""

    def get_language_scope_by_name(self, name: str) -> LanguageScope:
        """Return a :class:schemas.language_scope.LanguageScope by his subtag."""
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
        """Return the list of ExtLangs that are included in BCP47."""
        pass

    def get_ext_lang_by_subtag(self, subtag: str, case_sensitive: bool = False) -> ExtLang:
        """Return a ExtLang by his subtag."""
        try:
            return self._tag_or_subtag_filter(subtag, self.ext_langs, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ExtLangSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def scripts(self) -> List[Script]:
        """Return the list of Scripts that are included in BCP47."""
        pass

    def get_script_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Script:
        """Return a Script by his subtag.
        :raise exceptions.not_found.script_subtag_not_found_error.ScriptSubtagNotFoundError:"""
        try:
            return self._tag_or_subtag_filter(subtag, self.scripts, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise ScriptSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def regions(self) -> List[Region]:
        """Return the list of Scripts that are included in BCP47."""

    def get_region_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Region:
        """Return a Region by his subtag."""
        try:
            return self._tag_or_subtag_filter(subtag, self.regions, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise RegionSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def variants(self) -> List[Variant]:
        """Return the list of Variants that are included in BCP47."""

    def get_variant_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Variant:
        """Return a Variant by his subtag."""
        try:
            return self._tag_or_subtag_filter(subtag, self.variants, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise VariantSubtagNotFoundError(subtag) from e

    @property
    @abc.abstractmethod
    def grandfathered(self) -> List[Grandfathered]:
        """Return the list of Grandfathered that are included in BCP47."""

    def get_grandfathered_by_tag(self, tag: str, case_sensitive: bool = False) -> Grandfathered:
        """Return a Variant by his tag."""
        try:
            return self._tag_or_subtag_filter(tag, self.grandfathered, case_sensitive)
        except TagOrSubtagNotFoundError as e:
            raise GrandfatheredTagNotFoundError(tag) from e

    @property
    @abc.abstractmethod
    def redundant(self) -> List[Redundant]:
        """Return the list of Redundant that are included in BCP47."""
        pass

    def get_redundant_by_tag(self, tag: str, case_sensitive: bool = False) -> Redundant:
        """Return a Redundant by his tag."""
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

    def _tag_parser(self, tag: str,
                    case_sensitive: bool) -> Dict[str, Union[Language, ExtLang, Script, Region, Variant, ExtLang]]:
        """
        :raise exceptions.not_found.tag_or_subtag_not_found_error.TagOrSubtagNotFoundError:
        """
        i = 0
        tag_or_subtag_data = {}
        for subtag in tag.split('-'):
            while True:
                if i >= len(self._SUBTAG_DATA_FINDER):
                    raise TagOrSubtagNotFoundError(f"Subtag {subtag} of {tag} is not found.")
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

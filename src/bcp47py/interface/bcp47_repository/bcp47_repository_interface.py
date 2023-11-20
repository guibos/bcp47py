import abc
from typing import List

from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.subtags import Subtags
from schemas.variant import Variant


class BCP47RepositoryInterface(abc.ABC):

    @property
    @abc.abstractmethod
    def languages(self) -> List[Language]:
        """Return the list of Language that are included in BCP47."""

    @abc.abstractmethod
    def get_language_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Language:
        """Return a Language by his subtag.

        :raise from exceptions.invalid.base.invalid_data_error import InvalidDataErrorexceptions.not_found.language_subtag_not_found_error.LanguageSubtagNotFoundError:"""

    @property
    @abc.abstractmethod
    def languages_scopes(self) -> List[LanguageScope]:
        """Return the list of LanguageScope that are included in BCP47."""

    @abc.abstractmethod
    def get_language_scope_by_name(self, name: str) -> LanguageScope:
        """Return a LanguageScope by his subtag.

        :raise from exceptions.invalid.base.invalid_data_error import InvalidDataErrorexceptions.not_found.language_scope_not_found_error.LanguageScopeNotFoundError:
        :raise RuntimeError:"""

    @property
    @abc.abstractmethod
    def ext_langs(self) -> List[ExtLang]:
        """Return the list of ExtLangs that are included in BCP47."""

    @abc.abstractmethod
    def get_ext_lang_by_subtag(self, subtag: str, case_sensitive: bool = False) -> ExtLang:
        """Return a ExtLang by his subtag.

        :raise from exceptions.invalid.base.invalid_data_error import InvalidDataErrorexceptions.not_found.ext_lang_subtag_not_found_error.ExtLangSubtagNotFoundError:"""

    @property
    @abc.abstractmethod
    def scripts(self) -> List[Script]:
        """Return the list of Scripts that are included in BCP47."""

    @abc.abstractmethod
    def get_script_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Script:
        """Return a Script by his subtag.

        :raise from exceptions.invalid.base.invalid_data_error import InvalidDataErrorexceptions.not_found.script_subtag_not_found_error.ScriptSubtagNotFoundError:"""

    @property
    @abc.abstractmethod
    def regions(self) -> List[Region]:
        """Return the list of Scripts that are included in BCP47."""

    @abc.abstractmethod
    def get_region_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Region:
        """Return a Region by his subtag."""

    @property
    @abc.abstractmethod
    def variants(self) -> List[Variant]:
        """Return the list of Variants that are included in BCP47."""

    @abc.abstractmethod
    def get_variant_by_subtag(self, subtag: str, case_sensitive: bool = False) -> Variant:
        """Return a Variant by his subtag."""

    @property
    @abc.abstractmethod
    def grandfathered(self) -> List[Grandfathered]:
        """Return the list of Grandfathered that are included in BCP47."""

    @abc.abstractmethod
    def get_grandfathered_by_tag(self, tag: str, case_sensitive: bool = False) -> Grandfathered:
        """Return a Variant by his tag."""

    @property
    @abc.abstractmethod
    def redundant(self) -> List[Redundant]:
        """Return the list of Redundant that are included in BCP47."""

    @abc.abstractmethod
    def get_redundant_by_tag(self, tag: str, case_sensitive: bool = False) -> Redundant:
        """Return a Redundant by his tag."""

    @abc.abstractmethod
    def tag_parser(self, tag: str, case_sensitive: bool = False) -> Subtags:
        """Parse string tag to get all subtags."""

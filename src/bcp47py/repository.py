"""Repository that provides all data from BCP47."""

import dataclasses
import functools
from datetime import datetime
from typing import Optional, Dict, Any, Type, List, Union

from pydantic import ValidationError

from exceptions.invalid.invalid_ext_lang_data_error import InvalidExtLanguageDataError
from exceptions.invalid.invalid_grandfathered_data_error import InvalidGrandfatheredDataError
from exceptions.invalid.invalid_language_data_error import InvalidLanguageDataError
from exceptions.invalid.invalid_redundant_data_error import InvalidRedundantDataError
from exceptions.invalid.invalid_region_data_error import InvalidRegionDataError
from exceptions.invalid.invalid_registry_file_date_error import InvalidRegistryFileDate
from exceptions.invalid.invalid_script_data_error import InvalidScriptDataError
from exceptions.invalid.invalid_variant_data_error import InvalidVariantDataError
from exceptions.unexpected_bcp47.unexpected_bcp47_duplicated_key import UnexpectedBCP47DuplicatedKeyError
from exceptions.unexpected_bcp47.unexpected_bcp47_key_error import UnexpectedBCP47KeyError
from exceptions.unexpected_bcp47.unexpected_bcp47_key_type_error import UnexpectedBCP47KeyTypeError
from exceptions.unexpected_bcp47.unexpected_bcp47_missing_file_date_error import UnexpectedBCP47MissingFileDateError
from exceptions.unexpected_bcp47.unexpected_bcp47_missing_type_error import UnexpectedBCP47MissingTypeError
from exceptions.unexpected_bcp47.unexpected_bcp47_no_previous_key_error import UnexpectedBCP47NoPreviousKeyError
from exceptions.unexpected_bcp47.unexpected_bcp47_previous_data_type_error import UnexpectedBCP47PreviousDataTypeError
from exceptions.unexpected_bcp47.unexpected_bcp47_type_error import UnexpectedBCP47TypeError
from exceptions.unexpected_bcp47.unexpected_bcp47_value_error import UnexpectedBCP47ValueError
from mixin.base import Base
from base.repository_base import RepositoryBase
from enums.bcp47_type import BCP47Type
from enums.language_scope import LanguageScopeEnum
from schemas.ext_lang import ExtLang
from schemas.grandfathered import Grandfathered
from schemas.language import Language
from schemas.language_scope import LanguageScope
from schemas.redundant import Redundant
from schemas.region import Region
from schemas.script import Script
from schemas.variant import Variant


@dataclasses.dataclass
class _BCP47ValueType:
    """Helper dataclass that it structures the value of _BCP47_KEY_VALUE_TYPE_MAPPING dict."""
    value_type: Type
    internal_name: str


@dataclasses.dataclass
class _AddNewDataReturn:
    """Helper dataclass that it structures the return data from "_add_new_data" method."""
    data_dict: Dict[str, Any]
    previous_key: str


class Repository(RepositoryBase, Base):  # pylint: disable=too-many-instance-attributes
    """Repository that provides all data from the BCP47 specification in several dataclasses."""
    _BCP47_TYPE_PROCESSING_ORDER = [
        BCP47Type.SCRIPT, BCP47Type.LANGUAGE, BCP47Type.REGION, BCP47Type.VARIANT, BCP47Type.GRANDFATHERED,
        BCP47Type.REDUNDANT, BCP47Type.EXTLANG
    ]
    _BCP47_DEPENDENCY_FIELDS = [
        'macro_language',
        'preferred_value',
    ]
    _ITEM_SEPARATOR = '%%'
    _KEY_VALUE_SEPARATOR = ': '
    _FILE_HEADER = 'File-Date: '
    _BCP47_KEY_VALUE_TYPE_MAPPING: Dict[str, _BCP47ValueType] = {
        'Type': _BCP47ValueType(value_type=BCP47Type, internal_name='bcp_type'),
        'Subtag': _BCP47ValueType(value_type=str, internal_name='subtag'),
        'Description': _BCP47ValueType(value_type=list, internal_name='description'),
        'Suppress-Script': _BCP47ValueType(value_type=str, internal_name='suppress_script'),
        'Scope': _BCP47ValueType(value_type=str, internal_name='scope'),
        'Added': _BCP47ValueType(value_type=datetime, internal_name='added'),
        'Macrolanguage': _BCP47ValueType(value_type=str, internal_name='macro_language'),
        'Comments': _BCP47ValueType(value_type=list, internal_name='comments'),
        'Preferred-Value': _BCP47ValueType(value_type=str, internal_name='preferred_value'),
        'Deprecated': _BCP47ValueType(value_type=datetime, internal_name='deprecated'),
        'Prefix': _BCP47ValueType(value_type=list, internal_name='prefix'),
        'Tag': _BCP47ValueType(value_type=str, internal_name='tag'),
    }
    _languages_scopes = (LanguageScopeEnum.COLLECTION, LanguageScopeEnum.PRIVATE_USE, LanguageScopeEnum.MACRO_LANGUAGE,
                         LanguageScopeEnum.SPECIAL)

    def __init__(self, language_subtag_registry_file_path: Optional[str] = None):
        """Main constructor also call a method that load all the data in this instance.

        :raise exceptions.unexpected_bcp47_missing_file_date_error.UnexpectedBCP47MissingFileDateError:
        :raise exceptions.invalid.invalid_registry_file_date_error.InvalidRegistryFileDate:
        :raise exceptions.unexpected_bcp47_no_previous_key_error.UnexpectedBCP47NoPreviousKeyError:
        :raise exceptions.unexpected_bcp47_previous_data_type_error.UnexpectedBCP47PreviousDataTypeError:
        :raise exceptions.unexpected_bcp47_key_error.UnexpectedBCP47KeyError:
        :raise exceptions.unexpected_bcp47_duplicated_key.UnexpectedBCP47DuplicatedKeyError:
        :raise exceptions.unexpected_bcp47_value_error.UnexpectedBCP47ValueError:
        :raise exceptions.unexpected_bcp47_key_type_error.UnexpectedBCP47KeyTypeError:
        :raise exceptions.missing_bcp_type_error.MissingBCPTypeError:
        :raise exceptions.unexpected_bcp47_type_error.UnexpectedBCP47TypeError:
        :raise exceptions.invalid.invalid_language_data_error.InvalidLanguageDataError:
        :raise exceptions.invalid.invalid_ext_lang_error.InvalidExtLanguageDataError:
        :raise exceptions.invalid.invalid_script_data_error.InvalidScriptDataError:
        :raise exceptions.invalid.invalid_region_data_error.InvalidRegionDataError:
        :raise exceptions.invalid.invalid_variant_data_error.InvalidVariantDataError
        :raise exceptions.invalid.invalid_grandfathered_data_error.InvalidGrandfatheredDataError:
        :raise exceptions.invalid.invalid_redundant_data_error.InvalidRedundantDataError:"""
        super().__init__()
        self._language_subtag_registry_file_path = (language_subtag_registry_file_path
                                                    or self._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH)

        self._languages: List[Language] = []
        self._languages_scopes: List[LanguageScope] = []
        self._ext_langs: List[ExtLang] = []
        self._scripts: List[Script] = []
        self._regions: List[Region] = []
        self._variants: List[Variant] = []
        self._grandfathered: List[Grandfathered] = []
        self._redundant: List[Redundant] = []

        self._load_data()

    @property
    def languages(self) -> List[Language]:
        return self._languages

    @property
    def languages_scopes(self) -> List[LanguageScope]:
        return self._languages_scopes

    @property
    def ext_langs(self) -> List[ExtLang]:
        return self._ext_langs

    @property
    def scripts(self) -> List[Script]:
        return self._scripts

    @property
    def regions(self) -> List[Region]:
        return self._regions

    @property
    def variants(self) -> List[Variant]:
        return self._variants

    @property
    def grandfathered(self) -> List[Grandfathered]:
        return self._grandfathered

    @property
    def redundant(self) -> List[Redundant]:
        return self._redundant

    def _load_data(self):
        """Main function that is responsible to load all data in the instance.

        :raise exceptions.unexpected_bcp47_missing_file_date_error.UnexpectedBCP47MissingFileDateError:
        :raise exceptions.invalid.invalid_registry_file_date_error.InvalidRegistryFileDate:
        :raise exceptions.unexpected_bcp47_no_previous_key_error.UnexpectedBCP47NoPreviousKeyError:
        :raise exceptions.unexpected_bcp47_previous_data_type_error.UnexpectedBCP47PreviousDataTypeError:
        :raise exceptions.unexpected_bcp47_key_error.UnexpectedBCP47KeyError:
        :raise exceptions.unexpected_bcp47_duplicated_key.UnexpectedBCP47DuplicatedKeyError:
        :raise exceptions.unexpected_bcp47_value_error.UnexpectedBCP47ValueError:
        :raise exceptions.unexpected_bcp47_key_type_error.UnexpectedBCP47KeyTypeError:
        :raise exceptions.missing_bcp_type_error.MissingBCPTypeError:
        :raise exceptions.unexpected_bcp47_type_error.UnexpectedBCP47TypeError:
        :raise exceptions.invalid.invalid_language_data_error.InvalidLanguageDataError:
        :raise exceptions.invalid.invalid_ext_lang_error.InvalidExtLanguageDataError:
        :raise exceptions.invalid.invalid_script_data_error.InvalidScriptDataError:
        :raise exceptions.invalid.invalid_region_data_error.InvalidRegionDataError:
        :raise exceptions.invalid.invalid_variant_data_error.InvalidVariantDataError
        :raise exceptions.invalid.invalid_grandfathered_data_error.InvalidGrandfatheredDataError:
        :raise exceptions.invalid.invalid_redundant_data_error.InvalidRedundantDataError:"""
        self._load_languages_scopes()
        self._load_bcp47()

    def _load_languages_scopes(self):
        """Function that create :class:`bcp47py.schemas.language_scope.LanguageScope` instances for each value of
        :class:`bcp47py.enums.language_scope.LanguageScopeEnum` enum."""
        for language_scope in LanguageScopeEnum:
            self._languages_scopes.append(LanguageScope(scope=language_scope))

    def _load_bcp47(self):
        """Main function that is responsible to parse a "language subtag registry" file and load data into the
        instance.

        :raise exceptions.unexpected_bcp47_missing_file_date_error.UnexpectedBCP47MissingFileDateError:
        :raise exceptions.invalid.invalid_registry_file_date_error.InvalidRegistryFileDate:
        :raise exceptions.unexpected_bcp47_no_previous_key_error.UnexpectedBCP47NoPreviousKeyError:
        :raise exceptions.unexpected_bcp47_previous_data_type_error.UnexpectedBCP47PreviousDataTypeError:
        :raise exceptions.unexpected_bcp47_key_error.UnexpectedBCP47KeyError:
        :raise exceptions.unexpected_bcp47_duplicated_key.UnexpectedBCP47DuplicatedKeyError:
        :raise exceptions.unexpected_bcp47_value_error.UnexpectedBCP47ValueError:
        :raise exceptions.unexpected_bcp47_key_type_error.UnexpectedBCP47KeyTypeError:
        :raise exceptions.missing_bcp_type_error.MissingBCPTypeError:
        :raise exceptions.unexpected_bcp47_type_error.UnexpectedBCP47TypeError:
        :raise exceptions.invalid.invalid_language_data_error.InvalidLanguageDataError:
        :raise exceptions.invalid.invalid_ext_lang_error.InvalidExtLanguageDataError:
        :raise exceptions.invalid.invalid_script_data_error.InvalidScriptDataError:
        :raise exceptions.invalid.invalid_region_data_error.InvalidRegionDataError:
        :raise exceptions.invalid.invalid_variant_data_error.InvalidVariantDataError
        :raise exceptions.invalid.invalid_grandfathered_data_error.InvalidGrandfatheredDataError:
        :raise exceptions.invalid.invalid_redundant_data_error.InvalidRedundantDataError:"""
        with open(self._language_subtag_registry_file_path, 'r', encoding=self._LANGUAGE_SUBTAG_REGISTRY_ENCODING) as f:
            items = f.read().split(self._ITEM_SEPARATOR)

        updated_at = self._get_file_date(items.pop(0))
        items = [self._parse_item(item, updated_at) for item in items]
        items.sort(key=functools.cmp_to_key(self._sort_bcp47_items))

        for item in items:
            self._add_item(item)

    def _sort_bcp47_items(self, a: Dict[str, Any], b: Dict[str, Any]) -> int:
        """Comparison function to sort items of a "Language subtag registry". It is very important to sort the items due
        the processing could require other previous item."""
        if a['bcp_type'] != b['bcp_type']:
            a_index = self._BCP47_TYPE_PROCESSING_ORDER.index(a['bcp_type'])
            b_index = self._BCP47_TYPE_PROCESSING_ORDER.index(b['bcp_type'])
            sort_order = a_index - b_index
        elif a.get('preferred_value') is not None and b.get('preferred_value') is None:
            sort_order = 1
        elif a.get('preferred_value') is None and b.get('preferred_value') is not None:
            sort_order = -1
        elif a.get('prefix') is not None and b.get('prefix') is None:
            sort_order = 1
        elif a.get('prefix') is None and b.get('prefix') is not None:
            sort_order = -1
        elif a.get('scope') is not None and b.get('scope') is None:
            sort_order = -1
        elif a.get('scope') is None and b.get('scope') is not None:
            sort_order = 1
        elif a.get('prefix') is not None and a.get('prefix') is not None:
            if a.get('prefix') > b.get('prefix'):
                sort_order = 1
            elif a.get('prefix') < b.get('prefix'):
                sort_order = -1
            else:
                sort_order = 0
        else:
            sort_order = 0
        return sort_order

    def _get_file_date(self, text: str) -> datetime:
        """Return the 'File-Date' that is the version date from the "Language Subtag registry".

        :raise exceptions.unexpected_bcp47_missing_file_date_error.UnexpectedBCP47MissingFileDateError:
        :raise exceptions.invalid.invalid_registry_file_date_error.InvalidRegistryFileDate:"""
        if not text.startswith(self._FILE_HEADER):
            raise UnexpectedBCP47MissingFileDateError()
        try:
            return datetime.fromisoformat(text[11:-1])
        except ValueError as e:
            raise InvalidRegistryFileDate(text) from e

    def _parse_item(self, item: str, updated_at: datetime) -> Dict[str, Any]:
        """Parse an item from the "Language Subtag registry". It gets the field value pairs and return a dict. Also
        include the current version of "Language Subtag registry" (updated_at).

        :raise exceptions.unexpected_bcp47_no_previous_key_error.UnexpectedBCP47NoPreviousKeyError:
        :raise exceptions.unexpected_bcp47_previous_data_type_error.UnexpectedBCP47PreviousDataTypeError:
        :raise exceptions.unexpected_bcp47_key_error.UnexpectedBCP47KeyError:
        :raise exceptions.unexpected_bcp47_duplicated_key.UnexpectedBCP47DuplicatedKeyError:
        :raise exceptions.unexpected_bcp47_value_error.UnexpectedBCP47ValueError:
        :raise exceptions.unexpected_bcp47_key_type_error.UnexpectedBCP47KeyTypeError:"""
        data = {'updated_at': updated_at}
        previous_key: Optional[str] = None

        for value in item.strip().split("\n"):
            if value.startswith(' '):
                data = self._append_data(previous_key, data, value)
            else:
                add_new_data_return = self._add_new_data(data, value)
                data = add_new_data_return.data_dict
                previous_key = add_new_data_return.previous_key

        return data

    @staticmethod
    def _append_data(previous_key: Optional[str], data: Dict[str, Any], value: str) -> Dict[str, Any]:
        """Case of :func:repository.Repository._parse_item when a new line start with space. It occurs when the data
        surpasses the max column size and requires to break the line. If previous key is a list it should be
        concatenated with the last value of the list. If is string it is only required to be concatenated with the
        value of previous key.

        :raise exceptions.unexpected_bcp47_no_previous_key_error.UnexpectedBCP47NoPreviousKeyError:
        :raise exceptions.unexpected_bcp47_previous_data_type_error.UnexpectedBCP47PreviousDataTypeError:"""
        if not previous_key:
            raise UnexpectedBCP47NoPreviousKeyError()
        previous_data_type = type(data[previous_key])
        if previous_data_type == list:
            data[previous_key][-1] += value[1:]
        elif previous_data_type == str:
            data[previous_key] += value[1:]
        else:
            raise UnexpectedBCP47PreviousDataTypeError(previous_data_type)
        return data

    def _add_new_data(self, data_dict: Dict[str, Any], value: str) -> _AddNewDataReturn:
        """Case of :func:repository.Repository._parse_item when it is required to parse a new key value.

        :raise exceptions.unexpected_bcp47_key_error.UnexpectedBCP47KeyError:
        :raise exceptions.unexpected_bcp47_duplicated_key.UnexpectedBCP47DuplicatedKeyError:
        :raise exceptions.unexpected_bcp47_value_error.UnexpectedBCP47ValueError:
        :raise exceptions.unexpected_bcp47_key_type_error.UnexpectedBCP47KeyTypeError:
        """
        key, value = value.split(self._KEY_VALUE_SEPARATOR, 1)
        if not (value_type := self._BCP47_KEY_VALUE_TYPE_MAPPING.get(key)):
            raise UnexpectedBCP47KeyError(key)

        previous_key = value_type.internal_name

        if data_dict.get(value_type.internal_name) is not None and value_type.value_type != list:
            raise UnexpectedBCP47DuplicatedKeyError(key)

        if value_type.value_type == list:
            if data_dict_value := data_dict.get(value_type.internal_name):
                data_dict_value.append(value)
            else:
                data_dict[value_type.internal_name] = [value]
        elif value_type.value_type == datetime:
            data_dict[value_type.internal_name] = datetime.fromisoformat(value)
        elif value_type.value_type == str:
            data_dict[value_type.internal_name] = value
        elif value_type.value_type in (BCP47Type, LanguageScopeEnum):
            try:
                data_dict[value_type.internal_name] = value_type.value_type(value)
            except ValueError as e:
                raise UnexpectedBCP47ValueError(value, value_type.internal_name) from e
        else:
            raise UnexpectedBCP47KeyTypeError(value_type.value_type)
        return _AddNewDataReturn(data_dict=data_dict, previous_key=previous_key)

    def _add_item(self, data_dict: Dict[str, Any]):
        """From a dict item check the type and convert to a dataclass and loads in this object class.

        :raise exceptions.missing_bcp_type_error.MissingBCPTypeError:
        :raise exceptions.unexpected_bcp47_type_error.UnexpectedBCP47TypeError:
        :raise exceptions.invalid.invalid_language_data_error.InvalidLanguageDataError:
        :raise exceptions.invalid.invalid_ext_lang_error.InvalidExtLanguageDataError:
        :raise exceptions.invalid.invalid_script_data_error.InvalidScriptDataError:
        :raise exceptions.invalid.invalid_region_data_error.InvalidRegionDataError:
        :raise exceptions.invalid.invalid_variant_data_error.InvalidVariantDataError
        :raise exceptions.invalid.invalid_grandfathered_data_error.InvalidGrandfatheredDataError:
        :raise exceptions.invalid.invalid_redundant_data_error.InvalidRedundantDataError:"""
        try:
            bcp47_type: BCP47Type = data_dict.pop('bcp_type')
        except KeyError:
            raise UnexpectedBCP47MissingTypeError() from KeyError

        data_dict = self._replace_to_object(data_dict)

        if bcp47_type == BCP47Type.LANGUAGE:
            self._load_language(data_dict)
        elif bcp47_type == BCP47Type.EXTLANG:
            self._load_ext_lang(data_dict)
        elif bcp47_type == BCP47Type.SCRIPT:
            self._load_script(data_dict)
        elif bcp47_type == BCP47Type.REGION:
            self._load_region(data_dict)
        elif bcp47_type == BCP47Type.VARIANT:
            self._load_variant(data_dict)
        elif bcp47_type == BCP47Type.GRANDFATHERED:
            self._load_grandfathered(data_dict)
        elif bcp47_type == BCP47Type.REDUNDANT:
            self._load_redundant(data_dict)
        else:
            raise UnexpectedBCP47TypeError(bcp47_type)

    def _load_language(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.language.Language` dataclass. Finally append to the languages list.

        :raise exceptions.invalid.invalid_language_data_error.InvalidLanguageDataError:"""
        try:
            self._languages.append(Language(**data_dict))
        except ValidationError as e:
            raise InvalidLanguageDataError(data_dict) from e

    def _load_ext_lang(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.ext_lang.ExtLang`. Finally append to the ext languages list.

        :raise exceptions.invalid.invalid_ext_lang_error.InvalidExtLanguageDataError:"""
        try:
            self._ext_langs.append(ExtLang(**data_dict))
        except ValidationError as e:
            raise InvalidExtLanguageDataError(data_dict) from e

    def _load_script(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.script.Script`. Finally append to the scripts list.

        :raise exceptions.invalid.invalid_script_data_error.InvalidScriptDataError:"""
        try:
            self._scripts.append(Script(**data_dict))
        except ValidationError as e:
            raise InvalidScriptDataError(data_dict) from e

    def _load_region(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.region.Region`. Finally append to the region list.

        :raise exceptions.invalid.invalid_region_data_error.InvalidRegionDataError:"""
        try:
            self._regions.append(Region(**data_dict))
        except ValidationError as e:
            raise InvalidRegionDataError(data_dict) from e

    def _load_variant(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.variant.Variant`. Finally append to the variants list.

        :raise exceptions.invalid.invalid_variant_data_error.InvalidVariantDataError:"""
        try:
            self._variants.append(Variant(**data_dict))
        except ValidationError as e:
            raise InvalidVariantDataError(data_dict) from e

    def _load_grandfathered(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.grandfathered.Grandfathered`. Finally append to the grandfathered
        list.

        :raise exceptions.invalid.invalid_grandfathered_data_error.InvalidGrandfatheredDataError:"""
        try:
            self._grandfathered.append(Grandfathered(**data_dict))
        except ValidationError as e:
            raise InvalidGrandfatheredDataError(data_dict) from e

    def _load_redundant(self, data_dict: Dict[str, Any]):
        """Get dict data and loads to :class:`bcp47py.schemas.redundant.Redundant`. Finally append to the redundant list.

        :raise exceptions.invalid.invalid_redundant_data_error.InvalidRedundantDataError:"""
        try:
            self._redundant.append(Redundant(**data_dict))
        except ValidationError as e:
            raise InvalidRedundantDataError(data_dict) from e

    def _replace_to_object(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:
        """From dict data replace string values that should be references to objects.

        :raise exceptions.not_found.tag_or_subtag_not_found_error.TagOrSubtagNotFoundError:
        :raise exceptions.not_found.script_subtag_not_found_error.ScriptSubtagNotFoundError:
        :raise exceptions.not_found.language_subtag_not_found_error.LanguageSubtagNotFoundError:
        :raise exceptions.not_found.language_scope_not_found_error.LanguageScopeNotFoundError:
        :raise exceptions.not_found.language_subtag_not_found_error.LanguageSubtagNotFoundError:"""
        if preferred_value := data_dict.pop('preferred_value', None):
            data_dict['preferred_value'] = self._tag_parser(preferred_value, case_sensitive=True)

        if suppress_script := data_dict.pop('suppress_script', None):
            data_dict['suppress_script'] = self.get_script_by_subtag(suppress_script, case_sensitive=True)

        if macro_language := data_dict.pop('macro_language', None):
            data_dict['macro_language'] = self.get_language_by_subtag(macro_language, case_sensitive=True)

        if langauge_scope := data_dict.pop('scope', None):
            data_dict['scope'] = self.get_language_scope_by_name(langauge_scope)

        if prefix_s := data_dict.pop('prefix', None):
            data_dict['prefix'] = self._parse_prefix(prefix_s)

        return data_dict

    def _parse_prefix(
            self, prefix_list: List[str]) -> List[Dict[str, Union[Language, ExtLang, Script, Region, Variant, ExtLang]]]:
        """Parse a list of string subtags to a dict of name of va
        :raise exceptions.not_found.tag_or_subtag_not_found_error.TagOrSubtagNotFoundError:"""

        prefix_f = []

        for prefix in prefix_list:
            prefix_f.append(self._tag_parser(prefix, True))
        return prefix_f

"""Repository that provides all data from BCP47."""

import dataclasses
import functools
from datetime import datetime
from typing import Optional, Dict, Any, Type, List, Union

from mixin.base import Base
from abstract.repository_abstract import RepositoryAbstract
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


class Repository(RepositoryAbstract, Base):  # pylint: disable=too-many-instance-attributes
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
        'Comments': _BCP47ValueType(value_type=str, internal_name='comments'),
        'Preferred-Value': _BCP47ValueType(value_type=str, internal_name='preferred_value'),
        'Deprecated': _BCP47ValueType(value_type=datetime, internal_name='deprecated'),
        'Prefix': _BCP47ValueType(value_type=list, internal_name='prefix'),
        'Tag': _BCP47ValueType(value_type=str, internal_name='tag'),
    }
    _languages_scopes = (LanguageScopeEnum.COLLECTION, LanguageScopeEnum.PRIVATE_USE, LanguageScopeEnum.MACRO_LANGUAGE,
                         LanguageScopeEnum.SPECIAL)

    def __init__(self, language_subtag_registry_file_path: str):
        super().__init__()
        self._language_subtag_registry_file_path = (language_subtag_registry_file_path or
                                                    self._LANGUAGE_SUBTAG_REGISTRY_FILE_PATH)

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
        self._load_languages_scopes()
        self._load_bcp47()

    def _load_languages_scopes(self):
        for language_scope in LanguageScopeEnum:
            self._languages_scopes.append(LanguageScope(scope=language_scope))

    def _load_bcp47(self):
        with open(self._language_subtag_registry_file_path, 'r', encoding='utf-8') as f:
            items = f.read().split(self._ITEM_SEPARATOR)

        updated_at = self._get_file_date(items.pop(0))
        items = [self._parse_item(item, updated_at) for item in items]
        items.sort(key=functools.cmp_to_key(self._sort_bcp47_items))

        for item in items:
            self._add_item(item)

    def _sort_bcp47_items(self, a: Dict[str, Any], b: Dict[str, Any]) -> int:
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
        if not text.startswith(self._FILE_HEADER):
            raise RuntimeError("Unexpected file format: File-Date not found")
        try:
            return datetime.fromisoformat(text[11:-1])
        except ValueError as e:
            raise RuntimeError("Unexpected file format: File-Date format is not valid") from e

    def _parse_item(self, item: str, updated_at: datetime) -> Dict[str, Any]:
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
        if not previous_key:
            raise RuntimeError("There was no previous data to which it should be concatenated")
        previous_data_type = type(data[previous_key])
        if previous_data_type == list:
            data[previous_key][-1] += value[1:]
        elif previous_data_type == str:
            data[previous_key] += value[1:]
        else:
            raise RuntimeError("Unexpected previous data type with a data that must be appended")
        return data

    def _add_new_data(self, data_dict: Dict[str, Any], value: str) -> _AddNewDataReturn:
        key, value = value.split(self._KEY_VALUE_SEPARATOR, 1)
        if not (value_type := self._BCP47_KEY_VALUE_TYPE_MAPPING.get(key)):
            raise RuntimeError(f"Unexpected BCP47 key: {key}")

        previous_key = value_type.internal_name

        if data_dict.get(value_type.internal_name) is not None and value_type.value_type != list:
            raise RuntimeError(f"Unexpected file format: Value key {key} is duplicated")

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
                raise RuntimeError(f"Unexpected value type: {key}") from e
        else:
            raise RuntimeError(f"Value type {value_type.value_type} workflow is not properly "
                               f"programmed")
        return _AddNewDataReturn(data_dict=data_dict, previous_key=previous_key)

    def _add_item(self, data_dict: Dict[str, Any]):
        try:
            bcp_type = data_dict.pop('bcp_type')
        except KeyError:
            raise RuntimeError("Unexpected workflow bcp_type was not retrieved") from KeyError

        data_dict = self._replace_to_object(data_dict)

        if bcp_type == BCP47Type.LANGUAGE:
            self._load_language(data_dict)
        elif bcp_type == BCP47Type.EXTLANG:
            self._load_ext_lang(data_dict)
        elif bcp_type == BCP47Type.SCRIPT:
            self._load_script(data_dict)
        elif bcp_type == BCP47Type.REGION:
            self._load_region(data_dict)
        elif bcp_type == BCP47Type.VARIANT:
            self._load_variant(data_dict)
        elif bcp_type == BCP47Type.GRANDFATHERED:
            self._load_grandfathered(data_dict)
        elif bcp_type == BCP47Type.REDUNDANT:
            self._load_redundant(data_dict)
        else:
            raise RuntimeError(f"Unexpected workflow bcp_type unknown: {bcp_type}")

    def _load_language(self, data_dict: Dict[str, Any]):
        self._languages.append(Language(**data_dict))

    def _load_ext_lang(self, data_dict: Dict[str, Any]):
        self._ext_langs.append(ExtLang(**data_dict))

    def _load_script(self, data_dict: Dict[str, Any]):
        self._scripts.append(Script(**data_dict))

    def _load_region(self, data_dict: Dict[str, Any]):
        self._regions.append(Region(**data_dict))

    def _load_variant(self, data_dict: Dict[str, Any]):
        self._variants.append(Variant(**data_dict))

    def _load_grandfathered(self, data_dict: Dict[str, Any]):
        self._grandfathered.append(Grandfathered(**data_dict))

    def _load_redundant(self, data_dict: Dict[str, Any]):
        self._redundant.append(Redundant(**data_dict))

    def _replace_to_object(self, data_dict: Dict[str, Any]) -> Dict[str, Any]:
        if preferred_value := data_dict.pop('preferred_value', None):
            data_dict['preferred_value'] = self._tag_parser(preferred_value, case_sensitive=True)

        if suppress_script := data_dict.pop('suppress_script', None):
            data_dict['suppress_script'] = self.get_script_by_subtag(suppress_script, case_sensitive=True)

        if macro_language := data_dict.pop('macro_language', None):
            data_dict['macro_language'] = self.get_language_by_subtag(macro_language, case_sensitive=True)

        if langauge_scope := data_dict.pop('scope', None):
            data_dict['scope'] = self.get_language_scope_by_name(langauge_scope)

        if prefix_s := data_dict.pop('prefix', None):
            data_dict['prefix'] = self._parse_prefix(prefix_s, case_sensitive=True)

        return data_dict

    def _parse_to_object_preferred_value(self, bcp47_type: BCP47Type, data_dict: Dict[str, Any],
                                         preferred_value: str) -> Dict[str, Any]:
        if bcp47_type == BCP47Type.LANGUAGE:
            data_dict['preferred_value'] = self.get_language_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.EXTLANG:
            data_dict['preferred_value'] = self.get_ext_lang_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.SCRIPT:
            data_dict['preferred_value'] = self.get_script_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.REGION:
            data_dict['preferred_value'] = self.get_region_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.VARIANT:
            data_dict['preferred_value'] = self.get_variant_by_subtag(preferred_value)
        elif bcp47_type == BCP47Type.GRANDFATHERED:
            data_dict['preferred_value'] = self.get_grandfathered_by_tag(preferred_value)
        elif bcp47_type == BCP47Type.REDUNDANT:
            data_dict['preferred_value'] = self.get_redundant_by_tag(preferred_value)
        else:
            raise RuntimeError(f"Unexpected workflow bcp_type unknown: {bcp47_type}")
        return data_dict

    def _parse_prefix(
            self, prefix_list: List[str],
            case_sensitive: bool) -> List[Dict[str, Union[Language, ExtLang, Script, Region, Variant, ExtLang]]]:
        prefix_f = []

        for prefix in prefix_list:
            prefix_f.append(self._tag_parser(prefix, case_sensitive))
        return prefix_f

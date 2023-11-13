"""Common aliases of from exceptions.invalid.mixin.invalid_data_error import InvalidDataError"""

from typing import Union

from schemas.ext_lang import ExtLang, ExtLangPreferredValue
from schemas.grandfathered import Grandfathered, GrandfatheredPreferredValue
from schemas.language import Language, LanguagePreferredValue
from schemas.redundant import RedundantPreferredValue, Redundant
from schemas.region import Region, RegionPreferredValue
from schemas.script import Script
from schemas.variant import VariantPreferredValue, Variant

TagsType = Union[Grandfathered, Redundant]
SubtagType = Union[Script, Language, Region, ExtLang, Variant]
TagsOrSubtagType = Union[TagsType, SubtagType]
PreferredValuesType = Union[LanguagePreferredValue, RegionPreferredValue, ExtLangPreferredValue, VariantPreferredValue,
                            GrandfatheredPreferredValue, RedundantPreferredValue]

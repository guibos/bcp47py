"""PreferredValueValidator class tests."""

import datetime

import pytest
from pydantic import ValidationError

from schemas.region import Region, RegionPreferredValue


@pytest.fixture(scope='session')
def region_example() -> Region:
    """Region example to test as preferred value."""
    return Region(
        subtag='r',
        added=datetime.datetime.now(),
        updated_at=datetime.datetime.now(),
    )


def test_preferred_value_validator_all_none():
    """Test a normal scenario when the preferred value and deprecated are null."""
    Region(subtag='a',
           added=datetime.datetime.now(),
           updated_at=datetime.datetime.now(),
           preferred_value=None,
           deprecated=None)


def test_preferred_value_validator_is_deprecated():
    Region(subtag='a',
           added=datetime.datetime.now(),
           updated_at=datetime.datetime.now(),
           preferred_value=None,
           deprecated=datetime.datetime.now())


def test_preferred_value_validator_have_preferred_value(region_example: Region):
    Region(subtag='a',
           added=datetime.datetime.now(),
           updated_at=datetime.datetime.now(),
           preferred_value=RegionPreferredValue(region=region_example),
           deprecated=datetime.datetime.now())


def test_preferred_value_validator_invalid(region_example: Region):
    with pytest.raises(ValidationError):
        Region(subtag='a',
               added=datetime.datetime.now(),
               updated_at=datetime.datetime.now(),
               preferred_value=RegionPreferredValue(region=region_example),
               deprecated=None)

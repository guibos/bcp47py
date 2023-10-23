"""Module with PreferredValueValidator class."""

from pydantic import model_validator


class PreferredValueValidator:
    """Class with all validation related with "preferred value"."""

    @model_validator(mode='before')
    def deprecated_validator(cls, values):
        """Validate that when deprecated is set preferred value must be present in all cases."""
        if values.get('preferred_value') is not None and values.get('deprecated') is None:
            raise ValueError('Preferred_value is set but deprecated is not set')
        return values

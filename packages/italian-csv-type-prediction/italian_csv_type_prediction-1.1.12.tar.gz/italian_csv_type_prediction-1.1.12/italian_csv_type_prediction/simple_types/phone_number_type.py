import phonenumbers
from .string_type import StringType


class PhoneNumberType(StringType):

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches rules for Codice Fiscale values."""
        if super().validate(candidate, **kwargs):
            try:
                return phonenumbers.is_valid_number(phonenumbers.parse(candidate, "IT"))
            except phonenumbers.NumberParseException:
                pass
        return False

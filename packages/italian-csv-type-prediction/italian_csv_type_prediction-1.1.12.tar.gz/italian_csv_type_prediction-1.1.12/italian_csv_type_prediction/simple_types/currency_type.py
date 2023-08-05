from money_parser import price_str
from .string_type import StringType


class CurrencyType(StringType):
    def validate(self, candidate, **kwargs) -> bool:
        if not super().validate(candidate, **kwargs):
            return False
        try:
            candidate = price_str(str(candidate))
            return len(str(float(candidate)).split(".")[-1]) <= 2
        except (ValueError, TypeError):
            return False

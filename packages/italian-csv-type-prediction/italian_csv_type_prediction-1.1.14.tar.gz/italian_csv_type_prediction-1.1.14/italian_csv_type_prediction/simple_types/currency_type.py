from money_parser import price_str
from .string_type import StringType
from .float_type import FloatType
from .set_regex_type_predictor import SetRegexTypePredictor
from ..datasets import load_currency_starters

class CurrencyType(StringType):
    def __init__(self):
        super().__init__()
        self._float = FloatType()
        self._regex = SetRegexTypePredictor(load_currency_starters(), pattern=r"(?:\W|\b|\d)(?:{})(?:\W|\b|\d)")

    def validate(self, candidate, **kwargs) -> bool:
        if self._float.validate(candidate):
            return len(str(self._float.convert(candidate)).split(".")[-1]) <= 2
        try:
            if not self._regex.validate(candidate):
                return False
            candidate = price_str(str(candidate))
            return len(str(self._float.convert(candidate)).split(".")[-1]) <= 2
        except (ValueError, TypeError):
            return False

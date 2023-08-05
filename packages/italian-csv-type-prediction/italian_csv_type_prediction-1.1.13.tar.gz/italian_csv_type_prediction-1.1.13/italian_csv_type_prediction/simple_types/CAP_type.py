from .simple_type import SimpleTypePredictor
from .integer_type import IntegerType
from .integer_type import FloatType
from .regex_type_predictor import RegexTypePredictor


class CAPType(SimpleTypePredictor):

    def __init__(self):
        """Create new float type predictor based on regex."""
        super().__init__()
        self._predictor = RegexTypePredictor(r"^\d{5}$")
        self._integer = IntegerType()
        self._float = FloatType()

    def convert(self, candidate) -> str:
        """Convert given candidate to CAP."""
        if self._integer.validate(candidate):
            candidate = self._integer.convert(candidate)
        return str(candidate).zfill(5)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for CAP values."""
        if self._float.validate(candidate) and not self._integer.validate(candidate):
            # If it is an float but not an integer it is not a valid CAP.
            return False
        return self._predictor.validate(self.convert(candidate))
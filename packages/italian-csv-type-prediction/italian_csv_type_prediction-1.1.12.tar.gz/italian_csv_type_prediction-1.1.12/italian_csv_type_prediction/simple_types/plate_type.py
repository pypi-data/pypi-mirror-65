from .simple_type import SimpleTypePredictor
from .regex_type_predictor import RegexTypePredictor


class PlateType(SimpleTypePredictor):

    def __init__(self):
        """Create new float type predictor based on regex."""
        self._predictor = RegexTypePredictor(r"^[a-zA-Z]{2}[0-9]{2}[a-zA-z]{3}$")

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for float values."""
        return self._predictor.validate(candidate)

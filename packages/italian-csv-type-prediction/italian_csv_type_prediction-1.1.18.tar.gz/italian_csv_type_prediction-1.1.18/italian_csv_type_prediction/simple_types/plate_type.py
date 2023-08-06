from .simple_type import SimpleTypePredictor
from .regex_type_predictor import RegexTypePredictor


class PlateType(SimpleTypePredictor):

    def __init__(self):
        """Create new Plate type predictor based on regex."""
        self._predictor = RegexTypePredictor(r"^[a-zA-Z]{2}\s?[0-9]{3}\s?[a-zA-z]{2}$")

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for ."""
        return self._predictor.validate(candidate)

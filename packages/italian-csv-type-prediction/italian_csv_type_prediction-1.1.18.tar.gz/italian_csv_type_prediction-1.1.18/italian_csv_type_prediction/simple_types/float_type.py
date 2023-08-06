from .simple_type import SimpleTypePredictor
from .regex_type_predictor import RegexTypePredictor
from ..utils import normalize


class FloatType(SimpleTypePredictor):

    def __init__(self):
        """Create new float type predictor based on regex."""
        self._predictor = RegexTypePredictor(r"^-?(?:\d+|[,.]\d{3})+(?:[,.]\d+)?$")

    def convert(self, candidate, **kwargs):
        candidate = str(normalize(candidate)).replace(",", ".")
        candidate = candidate.replace('.', "", (candidate.count('.')-1))
        return float(candidate)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate matches regex for float values."""
        if str(candidate).startswith("0"):
            return False
        return self._predictor.validate(candidate)

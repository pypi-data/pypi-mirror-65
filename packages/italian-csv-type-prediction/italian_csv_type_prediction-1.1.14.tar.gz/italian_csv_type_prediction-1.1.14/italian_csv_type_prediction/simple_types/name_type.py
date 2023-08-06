from .string_type import StringType
from .set_type_predictor import SetTypePredictor
from ..datasets import load_names
from codicefiscale import codicefiscale


class NameType(StringType):

    def __init__(self, **kwargs):
        """Create new surname type predictor."""
        super().__init__()
        self._predictor = SetTypePredictor(load_names(), normalize_values=True, **kwargs)

    @property
    def fuzzy(self) -> bool:
        return True

    def validate(self, candidate, fiscal_code: str = None, **kwargs) -> bool:
        """Return boolean representing if given candidate is a valid italian name."""
        if not super().validate(candidate, **kwargs):
            return False
        if fiscal_code is None:
            return self._predictor.validate(candidate)

        characters = codicefiscale.decode(
            fiscal_code
        )["raw"]["name"]

        candidate = candidate.lower()

        for character in characters.rstrip("X").lower():
            if character not in candidate:
                return False
            candidate = candidate[candidate.index(character):]

        return True
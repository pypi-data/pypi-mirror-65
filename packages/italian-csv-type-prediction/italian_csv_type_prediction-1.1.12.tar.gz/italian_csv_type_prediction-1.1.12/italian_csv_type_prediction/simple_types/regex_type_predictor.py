from .simple_type import SimpleTypePredictor
import re


class RegexTypePredictor(SimpleTypePredictor):

    def __init__(self, pattern: str):
        """Create new regex based predictor.

        Parameters
        --------------------------------
        pattern: str,
            The pattern against which to test.
        """
        self._regex = re.compile(pattern)

    def validate(self, candidate) -> bool:
        """Return boolean representing if given candidate matches regex."""
        return bool(self._regex.match(str(candidate)))

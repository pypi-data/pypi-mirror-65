from .simple_type import SimpleTypePredictor


class StringType(SimpleTypePredictor):

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is a string"""
        return isinstance(candidate, str)

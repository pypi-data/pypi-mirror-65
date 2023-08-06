from .float_type import FloatType


class IntegerType(FloatType):

    def convert(self, candidate) -> int:
        """Cast given candidate to integer."""
        return int(super().convert(candidate))

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate can be considered integer."""
        return super().validate(candidate, **kwargs) and super().convert(candidate).is_integer()

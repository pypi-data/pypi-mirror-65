from .float_type import FloatType


class IntegerType(FloatType):

    def convert(self, candidate) -> int:
        """Cast given candidate to integer."""
        return int(float(str(candidate).replace(",", ".")))

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate can be considered integer."""
        return super().validate(candidate, **kwargs) and float(str(candidate).replace(",", ".")).is_integer()

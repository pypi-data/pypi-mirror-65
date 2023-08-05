from stdnum import get_cc_module
from .simple_type import SimpleTypePredictor
from .integer_type import IntegerType
from .float_type import FloatType


class IVAType(SimpleTypePredictor):
    def __init__(self):
        """Create new IVA type predictor based on rules."""
        super().__init__()
        self._vat_predictor = get_cc_module('it', 'iva')
        self._integer = IntegerType()
        self._float = FloatType()

    def convert(self, candidate):
        candidate = self._vat_predictor.compact(str(candidate))
        if self._integer.validate(candidate):
            candidate = self._integer.convert(candidate)
        return str(candidate).zfill(11)

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if given candidate is an IVA."""
        if self._float.validate(candidate) and not self._integer.validate(candidate):
            # If it is an float but not an integer it is not a valid CAP.
            return False
        return self._vat_predictor.is_valid(self.convert(candidate))

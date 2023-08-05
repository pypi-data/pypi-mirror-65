from .string_type import StringType
from ..datasets import load_address_starters
from ..utility import normalize


class AddressType(StringType):

    def __init__(self):
        super().__init__()
        self._starters = load_address_starters()

    def validate(self, candidate, **kwargs) -> bool:
        """Return boolean representing if candidate may be an italian address."""
        return super().validate(candidate) and any(normalize(candidate).startswith(start+" ") for start in self._starters)

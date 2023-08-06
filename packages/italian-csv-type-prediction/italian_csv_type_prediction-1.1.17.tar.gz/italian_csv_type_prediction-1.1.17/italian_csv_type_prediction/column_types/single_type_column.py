from typing import Dict

from ..simple_types import AddressType as SimpleAddressType
from ..simple_types import BiologicalSexType as SimpleBiologicalSexType
from ..simple_types import BooleanType as SimpleBooleanType
from ..simple_types import CAPType as SimpleCAPType
from ..simple_types import CodiceCatastoType as SimpleCodiceCatastoType
from ..simple_types import CodiceFiscaleType as SimpleCodiceFiscaleType
from ..simple_types import CountryCodeType as SimpleCountryCodeType
from ..simple_types import CountryType as SimpleCountryType
from ..simple_types import CurrencyType as SimpleCurrencyType
from ..simple_types import DateType as SimpleDateType
from ..simple_types import DocumentType as SimpleDocumentType
from ..simple_types import EMailType as SimpleEMailType
from ..simple_types import FloatType as SimpleFloatType
from ..simple_types import IntegerType as SimpleIntegerType
from ..simple_types import IVAType as SimpleIVAType
from ..simple_types import MunicipalityType as SimpleMunicipalityType
from ..simple_types import NameType as SimpleNameType
from ..simple_types import NaNType as SimpleNaNType
from ..simple_types import PhoneNumberType as SimplePhoneNumberType
from ..simple_types import PlateType as SimplePlateType
from ..simple_types import ProvinceCodeType as SimpleProvinceCodeType
from ..simple_types import RegionType as SimpleRegionType
from ..simple_types import StringType as SimpleStringType
from ..simple_types import SurnameType as SimpleSurnameType
from ..simple_types import YearType as SimpleYearType
from .set_type_column import SetTypeColumnPredictor


class AddressType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleAddressType(), generalizations=SimpleStringType(),
                         fuzzy_generalization_threshold=0.8)


class BiologicalSexType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleBiologicalSexType())


class BooleanType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleBooleanType())


class CAPType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCAPType())


class CodiceFiscaleType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCodiceFiscaleType(), others=SimpleIVAType(), min_threshold=0.95)


class CodiceCatastoType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCodiceCatastoType())


class CountryCodeType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCountryCodeType())


class CountryType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCountryType())


class CurrencyType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleCurrencyType())


class DateType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleDateType())


class DocumentType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleDocumentType(), generalizations=SimpleStringType())


class EMailType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleEMailType())


class FloatType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleFloatType())


class IntegerType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleIntegerType())


class IVAType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleIVAType(), others=SimpleCodiceFiscaleType(), min_threshold=0.95)


class MunicipalityType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleMunicipalityType())


class NameType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleNameType(), generalizations=SimpleStringType(), fuzzy_generalization_threshold=0.8)


class NaNType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleNaNType(), min_threshold=0)


class PhoneNumberType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimplePhoneNumberType())


class PlateType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimplePlateType())


class ProvinceCodeType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleProvinceCodeType())


class RegionType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleRegionType())


class StringType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleStringType())


class SurnameType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleSurnameType(), generalizations=SimpleStringType(), fuzzy_generalization_threshold=0.7)


class YearType(SetTypeColumnPredictor):
    def __init__(self):
        """Create new Predictor based on a single type."""
        super().__init__(SimpleYearType())

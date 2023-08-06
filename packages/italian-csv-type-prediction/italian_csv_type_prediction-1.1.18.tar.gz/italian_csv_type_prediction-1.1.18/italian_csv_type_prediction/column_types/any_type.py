from typing import Dict, List

from .column_type_predictor import ColumnTypePredictor
from .single_type_column import (AddressType, BiologicalSexType, BooleanType,
                                 CAPType, CodiceFiscaleType, CountryCodeType,
                                 CountryType, CurrencyType, DateType,
                                 DocumentType, EMailType, FloatType,
                                 IntegerType, IVAType, MunicipalityType,
                                 NameType, NaNType, PhoneNumberType, PlateType,
                                 ProvinceCodeType, RegionType, StringType,
                                 SurnameType, YearType, CodiceCatastoType
                                 )
from .numeric_id_type import NumericIdType


class AnyTypePredictor:
    def __init__(self):
        self._predictors = [
            predictor()
            for predictor in (
                AddressType, CAPType, CodiceFiscaleType, CountryCodeType,
                CountryType, CurrencyType, DateType, EMailType,
                FloatType, IntegerType, IVAType, DocumentType, NumericIdType,
                MunicipalityType, NameType, NaNType, PhoneNumberType,
                ProvinceCodeType, RegionType, StringType, SurnameType,
                YearType, BiologicalSexType, BooleanType, PlateType, CodiceCatastoType
            )
        ]

    @property
    def supported_types(self):
        """Return list of currently supported types."""
        return [
            predictor.name
            for predictor in self._predictors
        ]

    @property
    def predictors(self) -> List[ColumnTypePredictor]:
        return self._predictors

    def predict(self, values: List, fiscal_codes: List[str] = (), ivas: List[str] = (), **kwargs) -> Dict[str, List[bool]]:
        """Return prediction from all available type."""
        return {
            predictor.name: predictor.validate(
                values,
                fiscal_codes=fiscal_codes,
                ivas=ivas,
                **kwargs
            )
            for predictor in self._predictors
        }

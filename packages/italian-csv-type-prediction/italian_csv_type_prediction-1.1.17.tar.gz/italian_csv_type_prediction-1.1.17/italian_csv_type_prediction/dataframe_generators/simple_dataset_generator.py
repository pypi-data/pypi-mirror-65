from ..embedding import DataframeEmbedding
from ..simple_types.simple_type import SimpleTypePredictor
from random import randint, uniform, choice
import numpy as np
from tqdm.auto import trange
import pandas as pd
from random_csv_generator import random_csv
from ..datasets import (
    load_nan, load_names, load_regions, load_countries, load_country_codes,
    load_municipalities, load_surnames, load_provinces_codes, load_caps,
    load_codice_fiscale, load_iva, load_strings, load_email, load_phone,
    load_date, load_euro, load_address, load_biological_sex, load_boolean,
    load_document_types, load_plate, load_codice_catasto
)


class SimpleDatasetGenerator:

    def __init__(self):
        self._datasets = self._load_types_datasets()
        self._embedding = DataframeEmbedding()

    def _load_types_datasets(self):
        integers = np.random.randint(-1000000, 100000, size=1000)
        string_integers = integers.astype(str)
        float_integers = integers.astype(float)

        all_integers = integers.tolist() + string_integers.tolist() + \
            float_integers.tolist()

        floats = np.random.uniform(-1000000, 100000, size=1000)
        string_floats = floats.astype(str)

        all_floats = floats.tolist() + string_floats.tolist()

        years = np.random.randint(1990, 2030, size=1000)
        string_years = years.astype(str)
        float_years = years.astype(float)

        all_years = years.tolist() + string_years.tolist() + \
            float_years.tolist()

        names = load_names()
        surnames = load_surnames()
        self._nans = load_nan()

        datasets = {
            "CodiceFiscale": load_codice_fiscale(),
            "IVA": load_iva(),
            "CodiceCatasto": load_codice_catasto(),
            "Document": load_document_types(),
            "Plate": load_plate(),
            "Address": load_address(),
            "CAP": load_caps(),
            "ProvinceCode": load_provinces_codes(),
            "Region": load_regions(),
            "Municipality": load_municipalities(),
            "Year": all_years,
            "Integer": all_integers,
            "Float": all_floats,
            "Country": load_countries(),
            "CountryCode": load_country_codes(),
            "Name": names,
            "Surname": surnames,
            "String": load_strings(),
            "EMail": load_email(),
            "PhoneNumber": load_phone(),
            "Currency": load_euro(),
            "Date": load_date(),
            "BiologicalSex": load_biological_sex(),
            "Boolean": load_boolean()
        }

        return {
            key: np.array(value)
            for key, value in datasets.items()
        }

    def get_dataset(self, predictor: SimpleTypePredictor) -> np.ndarray:
        """Return dataset for given predictor."""
        if predictor.name == "NaN":
            return self._nans
        if predictor.name == "NumericId":
            base = randint(0, 100000)
            rows = randint(5, 100)
            return list(range(base, base+rows))
        return self._datasets[predictor.name]

    def random_nan(self, *args):
        return choice(self._nans)

    def generate_simple_dataframe(
        self,
        nan_percentage: float = 0.2,
        min_rows: int = 3,
        max_rows: int = 100,
        mix_codes: bool = True
    ):
        rows = randint(min_rows, max_rows)
        df = pd.DataFrame({
            key: np.random.choice(values, size=rows, replace=True)
            for key, values in self._datasets.items()
        })

        base = randint(1, 100000)
        df["NumericId"] = list(range(base, base+rows))

        rnd = random_csv(rows)

        df["Name"] = rnd["name"]
        df["Surname"] = rnd["surname"]
        df["CodiceFiscale"] = rnd["codice_fiscale"]

        types = pd.DataFrame(
            np.tile(np.array(df.columns), (len(df), 1)),
            columns=df.columns,
            index=df.index
        )

        if mix_codes and choice([True, False]):
            mask = np.random.randint(0, 2, size=df.shape[0], dtype=bool)
            swap_codice_fiscale = df.CodiceFiscale[mask].values
            swap_iva = df.IVA[mask].values
            df.loc[mask, "CodiceFiscale"] = swap_iva
            df.loc[mask, "IVA"] = swap_codice_fiscale
            types.loc[mask, "CodiceFiscale"] = "IVA"
            types.loc[mask, "IVA"] = "CodiceFiscale"
            column_to_drop = choice(["CodiceFiscale", "IVA"])
            df = df.drop(columns=column_to_drop)
            types = types.drop(columns=column_to_drop)

        if nan_percentage > 0:
            mask = np.random.choice([False, True], size=df.shape, p=[
                nan_percentage, 1-nan_percentage])
            types[np.logical_not(mask)] = "NaN"
            df = df.where(mask, other=self.random_nan)
        return df, types

    def _build(self):
        df, types = self.generate_simple_dataframe()
        return self._embedding.transform(df, types)

    def build(self, number: int = 1000, verbose: bool = True):
        """Creates and encodes a number of dataframe samples for training"""
        X, y = list(zip(*[
            self._build()
            for _ in trange(number, desc="Rendering dataset", disable=not verbose)
        ]))

        return np.vstack(X), np.concatenate(y)

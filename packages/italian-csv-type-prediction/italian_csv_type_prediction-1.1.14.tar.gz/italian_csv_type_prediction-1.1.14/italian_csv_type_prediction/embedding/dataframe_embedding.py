from ..column_types import AnyTypePredictor, IVAType, CodiceFiscaleType
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


class DataframeEmbedding:

    def __init__(self):
        self._predictor = AnyTypePredictor()
        self._encoder = LabelEncoder().fit(self._predictor.supported_types)
        self._ivas = IVAType()
        self._fiscal_codes = CodiceFiscaleType()

    def transform(self, df: pd.DataFrame, y: np.ndarray = None) -> np.ndarray:
        """Encode given dataframe into a vector space."""
        fiscal_codes = [None]*df.shape[0]
        ivas = [None]*df.shape[0]
        for column in df.columns:
            predictions = self._ivas.validate(df[column])
            if any(predictions):
                ivas = [
                    value if prediction else None
                    for value, prediction in zip(df[column].values, predictions)
                ]
                break

        for column in df.columns:
            predictions = self._fiscal_codes.validate(df[column])
            if any(predictions):
                fiscal_codes = [
                    value if prediction else None
                    for value, prediction in zip(df[column].values, predictions)
                ]

        X = pd.concat([
            pd.DataFrame(self._predictor.predict(
                df[column],
                fiscal_codes=fiscal_codes,
                ivas=ivas
            ))
            for column in df.columns
        ])
        if y is not None:
            return X, self._encoder.transform(y.T.values.ravel())
        return X

    def reverse_label_embedding(self, encoded_labels: np.ndarray, df: pd.DataFrame) -> np.ndarray:
        decoded_labels = self._encoder.inverse_transform(encoded_labels)

        decoded_labels = decoded_labels.reshape((df.shape[1], df.shape[0]))

        return pd.DataFrame(
            decoded_labels.T,
            columns=df.columns,
            index=df.index
        )

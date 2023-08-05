from ..simple_types import AnySimpleTypePredictor
from sklearn.preprocessing import LabelEncoder
import pandas as pd
import numpy as np


class DataframeEmbedding:

    def __init__(self):
        self._predictor = AnySimpleTypePredictor()
        self._encoder = LabelEncoder().fit(self._predictor.supported_types)

    def transform(self, df: pd.DataFrame, y: np.ndarray = None) -> np.ndarray:
        """Encode given dataframe into a vector space."""
        embedding = []
        for column in df.columns:
            predictions = pd.DataFrame([
                self._predictor.predict(value)
                for value in df[column]
            ])

            embedding.append(np.hstack([
                predictions,
                np.tile(predictions.mean(), (len(predictions), 1))
            ]))
        x = np.vstack(embedding)
        if y is not None:
            return x, self._encoder.transform(y.T.ravel())
        return x

    def reverse_label_embedding(self, encoded_labels:np.ndarray, df:pd.DataFrame)->np.ndarray:
        decoded_labels = self._encoder.inverse_transform(encoded_labels)

        decoded_labels = decoded_labels.reshape((df.shape[1], df.shape[0]))

        return pd.DataFrame(
            decoded_labels.T,
            columns=df.columns,
            index=df.index
        )
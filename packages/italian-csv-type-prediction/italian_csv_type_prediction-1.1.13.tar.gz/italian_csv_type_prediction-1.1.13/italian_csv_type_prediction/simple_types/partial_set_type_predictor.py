from .set_type_predictor import SetTypePredictor
from typing import List
import random
import math


class PartialSetTypePredictor(SetTypePredictor):

    def __init__(self, elements: List, dataset_percentage: float = 0.8, **kwargs):
        """Create new partial set based predictor.

        Parameters
        --------------------------------
        elements: List,
            List of elements to take in consideration.
         dataset_percentage: float = 0.8,
            Percentage of values from dataset to use.
            This is useful to simulate ignorance of complete set.
        """
        random.shuffle(elements)
        elements = elements[math.ceil(len(elements)*dataset_percentage):]
        super().__init__(elements, **kwargs)

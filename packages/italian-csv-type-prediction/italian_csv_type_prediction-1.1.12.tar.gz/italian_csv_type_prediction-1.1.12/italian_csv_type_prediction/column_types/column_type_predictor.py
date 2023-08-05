from typing import Dict, List


class ColumnTypePredictor:
    """
        A column type predictor is a predictor that
        tries to guess the type of an object by extrapolating
        on the type of the othe objects of the same column.

        This type of predictor mainly tries to avoid
        false negatives.
    """
    
    def validate(self, candidate, values:List, types:List[str], **kwargs: Dict) -> bool:
        """Return boolean representing if type is identified.

        Parameters
        -----------------------------------
        candidate,
            The candidate to be identified.
        values:List,
            List of other values in the column.
        types:List[str],
            List of other types in the column.
        kwargs:Dict,
            Additional features to be considered.
        """
        raise NotImplementedError(
            "Method validate must be implemented in child class."
        )

from typing import Dict, Tuple, Union


class Types:
    Features = Dict
    Prediction = Union[str, int, float, bool]
    PredictionProbs = Union[Dict, None]
    UniqueId = Union[str, None]
    CaptureStatus = Tuple[str, bool]
    PredictionEvent = Tuple[str, dict]
    Target = Union[str, int, float, bool]

import json
import math
import numpy as np
import pandas as pd

from azureml.studio.core.logger import get_logger

logger = get_logger(__name__)


def decode_nan(val):
    if val == {'isNan': True}:
        return np.nan
    return val


def encode_nan(val):
    if isinstance(val, float) and math.isnan(val):
        return {'isNan': True}
    return val


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, pd.Timestamp):
            return str(obj)
        else:
            return super(NpEncoder, self).default(obj)

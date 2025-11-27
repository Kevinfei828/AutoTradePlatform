import numpy as np

future_dtype = np.dtype([
    ('open', np.float64),
    ('high', np.float64),
    ('low', np.float64),
    ('close', np.float64)
])

day_max_len = 60 * 24
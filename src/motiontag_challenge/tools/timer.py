from contextlib import contextmanager
from timeit import default_timer
from typing import Optional
import numpy as np


@contextmanager
def elapsed_timer(round_to: Optional[int] = None):
    """
    Timer for measuring the duration of a function/block.
    Usage:
    with elapsed_timer(2) as timer:
        # do something
        print(f'job took {timer():.2f} seconds')

    Parameters
    ----------
    round_to: int (optional)
        digit to round the elapsed time to
    Returns
    -------
    float
        elapsed seconds
    """
    start = default_timer()
    elapser = lambda: (np.round(default_timer() - start, round_to)
                       if round_to else default_timer() - start)
    yield lambda: elapser()
    end = default_timer()
    elapser = lambda: (np.round(end - start, round_to)
                       if round_to else end - start)

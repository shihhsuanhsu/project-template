"""
Shih-Hsuan Hsu
Feb. 7, 2025
Create a FRED api client
"""

import random
from glob import glob
import pandas as pd
import fredapi


def fred_api_iter():
    """
    Returns a iterable of FRED API (useful when there are multiple FRED API keys).
    """
    # check how many API keys are available
    keys = glob("../../../secrets/fred*.txt")
    random.shuffle(keys)  # so that the keys are used in random order
    # load each API key
    for key in keys:
        with open(key, "r", encoding="utf-8") as f:
            yield fredapi.Fred(f.read().strip())


def search(serach_words: str, **kwargs) -> pd.DataFrame:
    """
    Search for data in FRED.
    """
    # load API key
    fred_iter = fred_api_iter()
    fred = next(fred_iter)

    while True:  # allow retry
        try:
            return fred.search(serach_words, **kwargs)
        except Exception as e:
            if "Too Many Requests" in str(e):
                fred = next(fred_iter, None)
                print(f"Rate limit reached. Switching to another API key. {e}")
                if fred is None:
                    raise (f"Out of API keys. {e}")
                continue
            else:
                raise e


def get_series(series_id: str, **kwargs) -> pd.DataFrame:
    """
    Get a series from FRED.
    """
    # load API key
    fred_iter = fred_api_iter()
    fred = next(fred_iter)

    while True:  # allow retry
        try:
            return fred.get_series(series_id, **kwargs)
        except Exception as e:
            if "Too Many Requests" in str(e):
                fred = next(fred_iter, None)
                print(f"Rate limit reached. Switching to another API key. {e}")
                if fred is None:
                    raise (f"Out of API keys. {e}")
                continue
            else:
                raise e

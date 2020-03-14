"""
This script contains utility methods for parsing html responses
"""

from typing import Callable


def strip_text(func: Callable) -> Callable:
    """
    a wrapper to strip text
    """

    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)

        if res is None:
            return None

        if type(res) is not list:
            return res.replace('\n', '').strip()

        return [parsed_text.replace('\n', '').strip() for parsed_text in res]

    return wrapper


def is_positiveinteger(s: str) -> bool:
    try:
        if int(s) > 0:
            return True
    except ValueError:
        return False
    return False

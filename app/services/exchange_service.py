import requests

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from functools import lru_cache


session = requests.Session()

retry_strategy = Retry(
    total=3,
    backoff_factor=1,
    status_forcelist=[429, 500, 502, 503, 504]
)

adapter = HTTPAdapter(max_retries=retry_strategy)

session.mount("https://", adapter)
session.mount("http://", adapter)


@lru_cache(maxsize=1)
def get_exchange_rates():
    """
    Fetch latest exchange rates.
    Base currency = INR
    """

    url = "https://api.frankfurter.app/latest?from=INR"

    response = session.get(url, timeout=10)

    response.raise_for_status()

    return response.json()


def get_usd_rate():
    """
    Returns INR -> USD exchange rate.
    """

    data = get_exchange_rates()

    return data["rates"]["USD"]
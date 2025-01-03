import requests
import logging
from typing import Optional

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class APIExtractor:
    """
    A class to handle data extraction from APIs.
    """

    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session = requests.Session()
        if api_key:
            self.session.headers.update()

    def fetch_company_income_statement(self, symbols: list, period: str = "annual"):
        responses = []
        for symbol in symbols:
            url = (
                self.base_url
                + "/api/v3/income-statement/"
                + symbol
                + "?period="
                + period
                + "&apikey="
                + self.api_key
            )
            response = requests.get(url=url)
            if response.status_code == 200:
                logger.log(logging.INFO, "Fetched Company with Symbol: " + symbol)
                responses.append(response.json())
            else:
                logger.log(
                    logging.INFO,
                    f"Error with Symbol {symbol} {response.status_code} {response.text}",
                )
                print(response.status_code)
                print(response.text)
        return responses

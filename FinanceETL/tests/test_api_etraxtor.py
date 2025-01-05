import os
from etl.extract import APIExtractor
from dotenv import load_dotenv

load_dotenv()


class TestAPIExctractor:
    def test_fetch_company(self):
        base_url = str(os.getenv("BASE_URL"))
        api_key = os.getenv("API_KEY")
        api = APIExtractor(base_url=base_url, api_key=api_key)
        print("API_KEY")
        print(api_key)
        symbols = ["DQ", "NOVA", "ENPH", "JKS", "RUN", "CSIQ", "NVDA"]
        companies = api.fetch_company_income_statement(symbols=symbols)
        print(companies)

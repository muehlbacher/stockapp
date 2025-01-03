import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from etl.transform import DataTransformer
from etl.extract import APIExtractor
from etl.load import DataLoader

load_dotenv()


class TestAPITransform:
    def test_transform_company(self):
        base_url = str(os.getenv("BASE_URL"))
        api_key = os.getenv("API_KEY")
        api = APIExtractor(base_url=base_url, api_key=api_key)
        print("API_KEY")
        print(api_key)
        # symbols = ["CSIQ", "NVDA"]
        symbols = ["INTC"]
        symbols = ["AAPL"]
        companies_raw = api.fetch_company_income_statement(symbols=symbols)
        companies = DataTransformer().transform_company(companies_raw)
        print(companies)
        print(len(companies))
        print(print("Column Names:", companies.columns.tolist()))
        DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
        # Create the engine and session
        engine = create_engine(DATABASE_URL)
        Session = sessionmaker(bind=engine)
        session = Session()

        data_loader = DataLoader(db_session=session)
        data_loader.load_companies(companies)

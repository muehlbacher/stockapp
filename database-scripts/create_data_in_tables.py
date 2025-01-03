import os
from dotenv import load_dotenv
from pathlib import Path
import requests
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from indicators.warren_buffet import WarrenBuffets
from models.models import Company, StatementType, Metric, TimePeriod, FinancialData

# Get the parent directory of the current file (notebook)
parent_dir = Path().resolve().parent

# Specify the path to the .env file
dotenv_path = parent_dir / '.env'

# Load the .env file
load_dotenv(dotenv_path=dotenv_path)
# Verify by accessing an environment variable
print(os.getenv('API_KEY'))
API_KEY = os.getenv('API_KEY')

#get company id
DATABASE_URL = "mysql+pymysql://root:root@localhost/market"
# Create the engine and session
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()


def get_financial_statements(company_symbols: list) -> list:
    responses = []
    for symbol in company_symbols:
        url ="https://financialmodelingprep.com/api/v3/income-statement/" 
        url = url + symbol + "?period=annual&apikey=" + API_KEY
        response= requests.get(url=url)
        if response.status_code == 200:
            print("Fetched Company with Symbol: " + symbol)
            responses.append(response.json())
        else:
            print("Error with Symbol " + symbol)
            print(response.status_code)
            print(response.text)
    return responses

def check_company(company_symbol: str):
    try:
        id = session.query(Company).filter_by(Ticker=company_symbol).first().CompanyID
    except AttributeError as e:
        # company not found in the database
        # get company information from api and put it in the database
        # name, industry, sector, country, currency, description
        return None
    
def check_metric(metric_name: str):
   try:
       id = session.query(Metric).filter_by() 

    except Exception as ex:
        print("error in session query!")


if __name__ == "__main__":

    wb = WarrenBuffets()

    #load data from api
    #get a list of dicts with company information
    companies = get_financial_statements(['AAPL'])
    print(companies)

    #calculate the warren buffets per company
    for company in companies:
        df = pd.DataFrame(company)
        print(df)
        df = wb.applyAll(df)
        print(df)
        print(df['sgaRatio'])
        check_company(df['symbol'].iloc[0])


    #load the data in the database
    # check if company is already in Company
    # check if metric is already in Metric
    # check if year is already in TimePeriod
    # check if statementtype is already in StatementType

    # check if data is already in FinancialData



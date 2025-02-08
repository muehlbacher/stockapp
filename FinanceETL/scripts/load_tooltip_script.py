import os
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

from FinanceETL.etl.load.load_tooltip import TooltipLoader

load_dotenv()

if __name__ == "__main__":
    DATABASE_URL = os.getenv("DATABASE_URL")
    # Create the engine and session
    engine = create_engine(DATABASE_URL)
    Session = sessionmaker(bind=engine)
    session = Session()

    loader = TooltipLoader(session)

    loader.remove_tooltip("revenue")
    loader.remove_tooltip("GrossProfitMargin")
    tooltip = "The amount of money that came in the door during the period of time in question. If we manufacturing cars and we sell $120 million worth of cars in a year, we will report $120 million total revenue."
    loader.load_tooltip(metric_name="revenue", tooltip=tooltip)

    tooltip = "Gross Profit / Total Revenue = GPM;\n What creates a high gross profit margin is the company's durable competitive advantage, which allows it the freedom to price the products and services it sells well in excess of its cost of goods sold."
    loader.load_tooltip(metric_name="GrossProfitMargin", tooltip=tooltip)

    tooltip = "The companies hard costs. Research and Development of new products, selling and administrative costs of getting the product to market, ... "
    loader.load_tooltip(metric_name="operatingExpenses", tooltip=tooltip)

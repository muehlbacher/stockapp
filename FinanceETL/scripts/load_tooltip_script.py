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

    tooltip = "The amount of money that came in the door during the period of time in question. If we manufacturing cars and we sell $120 million worht of cars in a year, we will report $120 million total revenue."
    loader.load_tooltip(metric_name="revenue", tooltip=tooltip)

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
    loader.remove_tooltip("operatingExpenses")
    loader.remove_tooltip("costOfRevenue")
    loader.remove_tooltip("GrossProfit")
    loader.remove_tooltip("operatingIncome")

    tooltip = "The amount of money that came in the door during the period of time in question. If we manufacturing cars and we sell $120 million worth of cars in a year, we will report $120 million total revenue."
    loader.load_tooltip(metric_name="revenue", tooltip=tooltip)

    tooltip = "Gross Profit / Total Revenue = GPM;\n What creates a high gross profit margin is the company's durable competitive advantage, which allows it the freedom to price the products and services it sells well in excess of its cost of goods sold."
    loader.load_tooltip(metric_name="GrossProfitMargin", tooltip=tooltip)

    tooltip = "The companies hard costs. Research and Development of new products, selling and administrative costs of getting the product to market, ... "
    loader.load_tooltip(metric_name="operatingExpenses", tooltip=tooltip)

    tooltip = "costs (raw goods, labor). This number alone doesn't give us a clue about the companies durable competitive advantage. You have to look also at the Gross profit Always investigate exactly what the company is including in its calculation of its cost of sales. This gives us a good idea of how management is thinking about the business."
    loader.load_tooltip(metric_name="costOfRevenue", tooltip=tooltip)

    tooltip = "revenue - cost of revenue. Gross Profit is how much money the company made after subtracting the costs (raw goods, labor) used to make the goods. Doesn't include: sga, deprecation, interest cost."
    loader.load_tooltip(metric_name="GrossProfit", tooltip=tooltip)

    tooltip = "Gross Profit - Operating Expense"
    loader.load_tooltip(metric_name="operatingIncome", tooltip=tooltip)

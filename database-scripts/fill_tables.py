import pandas as pd
import pickle

import sys
import os
# Add the parent directory to the sys.path
parent_directory = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_directory)
# Now you can import the module from the parent folder
from indicators.warren_buffet import WarrenBuffets

def load_data():
    wb = WarrenBuffets()
    with open('../data/solar_companies_data.pkl', 'rb') as file:
        companies_data = pickle.load(file)

    print("FILE LOADED")

    companies_data_short = {}

    print(pd.DataFrame(companies_data))
    symbols=[]
    for key, item in companies_data.items():
        print("KEY")
        print(key)
        symbols.append(key)
        for year in item:
            companies_data_short[key] = [{'calendarYear': year['calendarYear'],
                                        'name': year['name'],
                                        'revenue': year['revenue'],
                                        'costOfRevenue': year['costOfRevenue'],
                                        'grossProfit': year['grossProfit'],
                                        'grossProfitRatio': year['grossProfitRatio'],
                                        'researchAndDevelopmentExpenses': year['researchAndDevelopmentExpenses'],
                                        'sellingGeneralAndAdministrativeExpenses': year['sellingGeneralAndAdministrativeExpenses'],
                                        'otherExpenses': year['otherExpenses'],
                                        'operatingExpenses': year['operatingExpenses'],
                                        'interestIncome': year['interestIncome'],
                                        'interestExpense': year['interestExpense'],
                                        'depreciationAndAmortization': year['depreciationAndAmortization'],
                                        'operatingIncome': year['operatingIncome'],
                                        'incomeBeforeTax': year['incomeBeforeTax'],
                                        'netIncome': year['netIncome'],
                                        'netIncomeRatio': year['netIncomeRatio']}
                                        for year in item]
            
    dataframes=[]        

    for symbol in symbols:
        df = pd.DataFrame(companies_data_short[symbol])
        df['company'] = symbol
        df = wb.applyAll(df)
        df = df.sort_values(by='calendarYear', ascending=True)
        dataframes.append(df)

    df = pd.concat(dataframes, ignore_index=True)
    columns_to_move = ['calendarYear', 'revenue', 'grossProfitRatio', 'sgaRatio']
    remaining_columns = [col for col in df.columns if col not in columns_to_move]
    new_column_order = columns_to_move + remaining_columns
    df = df[new_column_order]
    return df

if __name__ == "__main__":
    df = load_data()
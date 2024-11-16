import plotly.express as px
from django.shortcuts import render
import pickle
import pandas as pd
from .indicators import WarrenBuffets

def plotly_graph(request):
    df = load_data()
    print(df)
    # Sample data for a Plotly graph (replace this with your own data)

    filtered_df = df[df['company'] == 'DQ']
    fig = px.line(filtered_df, x='calendarYear', y='revenue', title='Revenue Over Time')

    # Generate the HTML for the Plotly graph
    graph_html = fig.to_html(full_html=False)

    return render(request, 'myapp/plotly_graph.html', {'graph_html': graph_html, 
                                                       'header_graph': "This is a graph"})


def load_data():
    wb = WarrenBuffets()
    with open('data/solar_companies_data.pkl', 'rb') as file:
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

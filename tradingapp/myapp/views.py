import plotly.express as px
from django.shortcuts import render
import pickle
import pandas as pd
#from .indicators import WarrenBuffets
from .forms import MyForm
from .models import Company
from .tables import CompanyTable
from django_tables2 import RequestConfig



def plotly_graph(request):
    df = load_data()

    print(df)
    selected_option = None
    unique_pairs = df.drop_duplicates(subset=['company'])[['company', 'name']]
    # Convert to a list of tuples
    choices = list(zip(unique_pairs['company'], unique_pairs['name']))
    print(type(choices))
    print(choices)

    if request.method == 'POST':
        form = MyForm(request.POST, choices=choices)
        if form.is_valid():
            selected_option = form.cleaned_data['dropdown']
            print(selected_option)
            # Handle the form data as needed
    else:
        form = MyForm(choices=choices)


    if selected_option:
        filtered_df = df[df['company'] == selected_option]
        company_name = df.loc[df['company'] == selected_option, 'name'].iloc[0]
    else:
        company_name = df.loc[df['company'] == "DQ", 'name'].iloc[0]
        filtered_df = df[df['company'] == 'DQ']


    fig1 = px.line(filtered_df, x='calendarYear', y='revenue', title='Revenue Over Time')
    fig2 = px.line(filtered_df, x='calendarYear', y='sgaRatio', title='SGA Ratio - Selling, General & Admission per Gross Profit')
    fig3 = px.line(filtered_df, x='calendarYear', y='randdRatio', title='Research and Development per Gross Profit')


    # Generate the HTML for the Plotly graph
    graph_html1 = fig1.to_html(full_html=False)
    graph_html2 = fig2.to_html(full_html=False)
    graph_html3 = fig3.to_html(full_html=False)

    #table_html = filtered_df.to_html(classes='table table-striped')
    companies_data = filtered_df.to_dict(orient='records')
    table = CompanyTable(companies_data)
    
    # Add pagination to the table if needed
    RequestConfig(request, paginate={"per_page": 10}).configure(table)


    return render(request, 'myapp/plotly_graph.html', {'table': table,
                                                       'graph_html1': graph_html1,
                                                       'graph_html2': graph_html2,
                                                       'graph_html3': graph_html3,
                                                       'header_graph': f"{company_name}",
                                                       'form': form})


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



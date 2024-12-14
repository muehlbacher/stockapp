import plotly.express as px
from django.shortcuts import render
import pickle
import pandas as pd
#from .indicators import WarrenBuffets
from .forms import MyForm
from .models.company_model import Company
from .models.financialdata_model import FinancialData
from .models.metric_model import Metric
from django_tables2 import RequestConfig



def plotly_graph(request):
    #df = load_data()
    ticker = 'CSIQ'

    companies = fetch_companies_name_and_ticker()
    # # Convert to a list of tuples
    choices = [(company['Ticker'], company['Name']) for company in companies]
    print("Choices:")
    print(choices)
    selected_option=None
    if request.method == 'POST':
         form = MyForm(request.POST, choices=choices)
         if form.is_valid():
             selected_option = form.cleaned_data['dropdown']
             print(selected_option)
             # Handle the form data as needed
    else:
         form = MyForm(choices=choices)
    if selected_option:
        ticker=selected_option
    df =fetch_data_from_db(ticker)
    print(df)
    table_data, avail_years = prepare_table_data(ticker)

    if isinstance(table_data, str):  # Check if it's an error message
        return render(request, 'error.html', {'error_message': table_data})
    metrics = fetch_metrics_wb()
    graphs = []
    for metric in metrics:
        graph_data =  fetch_graph_data(ticker, metric.MetricName)
        fig = px.line(graph_data, x='calendarYear', y=metric.MetricName, title=metric.MetricName)
        graphs.append(fig.to_html(full_html=False))

    return render(request, 'myapp/graph_financials.html', {'table_data': table_data, 
                                                           'company_name': ticker, 
                                                           'avail_years': avail_years,
                                                           'form': form,
                                                           'graphs': graphs,})

def fetch_graph_data(company_ticker, metric):
    # Fetch the company based on the ticker (or you could use Name)
    company = Company.objects.get(Ticker=company_ticker)

    # Fetch the 'Revenue' metric from the Metric model
    revenue_metric = Metric.objects.get(MetricName=metric)
   # Fetch the financial data for this company, where the metric is 'Revenue'
    financial_data = FinancialData.objects.filter(
        CompanyID=company,
        MetricID=revenue_metric
    ).select_related('TimePeriodID')  # Ensure to fetch the related TimePeriod

    # Prepare the data into a format suitable for Plotly (DataFrame)
    data = financial_data.values('TimePeriodID__Year', 'Value')  # Get calendar year and revenue value

    # Convert to pandas DataFrame
    df = pd.DataFrame(data)

    # Rename columns to match the graph's expected names
    df = df.rename(columns={'TimePeriodID__Year': 'calendarYear', 'Value': metric})


    return df


def fetch_companies_name_and_ticker():
    companies = Company.objects.values('Ticker', 'Name')
    print("---"*20)
    print(companies)
    print("---"*20)
    return companies

def prepare_table_data(ticker):
    """
    Fetch financial data for a given company and prepare it in a tabular format.
    
    Args:
        company_name (str): The name of the company to fetch data for.
    
    Returns:
        dict: A dictionary containing the tabular data (or an error message).
    """
    try:
        # Retrieve the company object
        company = Company.objects.get(Ticker=ticker)
      # Fetch all related financial data
        financial_data = FinancialData.objects.filter(CompanyID=company).select_related(
            'StatementTypeID', 'MetricID', 'TimePeriodID'
        )

        # Prepare the data for the DataFrame
        data = []
        for entry in financial_data:
            data.append({
                'Year': entry.TimePeriodID.Year,
                'Metric': entry.MetricID.MetricName,
                'Value': entry.Value,
            })

        # Create a DataFrame
        df = pd.DataFrame(data)
        print(df)
        unique_years = df['Year'].unique()


        # Pivot the DataFrame to have metrics as rows and years as columns
        pivot_table = df.pivot_table(
            index='Metric',  # Rows: Metrics
            columns='Year',  # Columns: Years
            values='Value',  # Values: Financial Data
            aggfunc='sum'    # Aggregate function (sum in case of duplicates)
        ).fillna(0)  # Replace NaN with 0

        # Convert to dictionary for Django template (now years are columns)
        table_data = pivot_table.to_dict(orient='index')
        
        return table_data, unique_years

    except Company.DoesNotExist:
        return f"Company with name '{ticker}' does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def fetch_data_from_db(ticker):
    """
    Fetch financial data for a given company across all years.
    
    Args:
        ticker (str): The name of the company to fetch data for.
    
    Returns:
        list: A list of dictionaries containing financial data and related information.
    """
    try:
        # Retrieve the company object
        company = Company.objects.get(Ticker=ticker)
        print(company)
        
        # Fetch all related financial data
        financial_data = FinancialData.objects.filter(CompanyID=company).select_related(
            'StatementTypeID', 'MetricID', 'TimePeriodID'
        )
        print(financial_data)
        
        # Prepare the data for the DataFrame
        data = []
        for entry in financial_data:
            data.append({
                'Company': company.Name,
                'StatementType': entry.StatementTypeID.StatementName,
                'Metric': entry.MetricID.MetricName,
                #'MetricType': entry.MetricID.MetricType,
                'Year': entry.TimePeriodID.Year,
                'Quarter': entry.TimePeriodID.Quarter,
                'StartDate': entry.TimePeriodID.StartDate,
                'EndDate': entry.TimePeriodID.EndDate,
                'Value': entry.Value,
            })

        print(data)
        
        df = pd.DataFrame(data)
        print(df)
        return df

    except Company.DoesNotExist:
        return f"Company with name '{ticker}' does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"    

def fetch_metrics_wb():
    return Metric.objects.filter(MetricType="wb").all()




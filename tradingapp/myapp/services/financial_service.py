import pandas as pd

from myapp.models.company_model import Company
from myapp.models.financialdata_model import FinancialData
from myapp.models.metric_model import Metric


class CompanyDoesNotExistError(Exception):
    pass


def fetch_graph_data(company_ticker, metric):
    company = Company.objects.get(Ticker=company_ticker)
    revenue_metric = Metric.objects.get(MetricName=metric)

    financial_data = FinancialData.objects.filter(
        CompanyID=company, MetricID=revenue_metric
    ).select_related("TimePeriodID")

    data = financial_data.values("TimePeriodID__Year", "Value")
    df = pd.DataFrame(data).rename(
        columns={"TimePeriodID__Year": "calendarYear", "Value": metric}
    )

    return df


def prepare_table_data_selected_metrics(ticker, metrics=None):
    if not metrics:
        metrics = [
            "revenue",
            "costOfRevenue",
            "grossProfit",
            "operatingExpenses",
            "sellingGeneralAndAdministrativeExpenses",
            "researchAndDevelopmentExpenses",
            "depreciationAndAmortization",
        ]

    try:
        results = (
            FinancialData.objects.select_related("MetricID", "TimePeriodID")
            .filter(CompanyID__Ticker=ticker, MetricID__MetricName__in=metrics)
            .values("MetricID__MetricName", "TimePeriodID__Year", "Value", "Valuation")
        )
        if not results:
            raise Company.DoesNotExist()
        # Convert query results into a DataFrame
        df = pd.DataFrame.from_records(results)
        if df.empty:
            return {}, []  # Return empty data if no records found

        # Sort DataFrame by Year (Descending) and then by Metric
        df.sort_values(
            by=["TimePeriodID__Year", "MetricID__MetricName"],
            ascending=[False, True],
            inplace=True,
        )

        # Transform data into a nested dictionary format
        metric_data = {
            metric: {
                str(row["TimePeriodID__Year"]): {
                    "value": f"{row['Value']:,.0f}",
                    "class": f"valuation-{row['Valuation']}",
                }
                for _, row in group.iterrows()
            }
            for metric, group in df.groupby("MetricID__MetricName")
        }

        unique_years = sorted(df["TimePeriodID__Year"].unique(), reverse=True)
        print(unique_years)
        return metric_data, unique_years

    except Company.DoesNotExist as e:
        raise CompanyDoesNotExistError(
            f"Company with ticker '{ticker}' does not exist."
        ) from e
    except Exception as e:
        return f"An error occurred: {str(e)}", []


def prepare_table_data(ticker):
    try:
        results = (
            FinancialData.objects.select_related("MetricID", "TimePeriodID")
            .filter(CompanyID__Ticker=ticker)
            .values("MetricID__MetricName", "TimePeriodID__Year", "Value", "Valuation")
        )

        print("DATA TABLE:--------")
        print(results)
        df = pd.DataFrame.from_records(results)
        if df.empty:
            return {}, []  # Return empty data if no records found

        # Sort DataFrame by Year (Descending) and then by Metric
        df.sort_values(
            by=["TimePeriodID__Year", "MetricID__MetricName"],
            ascending=[False, True],
            inplace=True,
        )

        # Transform data into a nested dictionary format
        metric_data = {
            metric: {
                str(row["TimePeriodID__Year"]): {
                    "value": row["Value"],
                    "class": f"valuation-{row['Valuation']}",
                }
                for _, row in group.iterrows()
            }
            for metric, group in df.groupby("MetricID__MetricName")
        }

        unique_years = sorted(df["TimePeriodID__Year"].unique(), reverse=True)
        print(unique_years)
        return metric_data, unique_years

    except Company.DoesNotExist:
        return f"Company with ticker '{ticker}' does not exist.", []
    except Exception as e:
        return f"An error occurred: {str(e)}"


def prepare_wb_table_data(ticker):
    try:
        # Define required metrics
        metrics = [
            "sgaRatio",
            "randdRatio",
            "deprecationRatio",
            "interestExpenseRatio",
            "netEarningsRatio",
        ]

        # Fetch financial data for the given company and metrics
        results = (
            FinancialData.objects.select_related("MetricID", "TimePeriodID")
            .filter(CompanyID__Ticker=ticker, MetricID__MetricName__in=metrics)
            .values("MetricID__MetricName", "TimePeriodID__Year", "Value", "Valuation")
        )
        print("WARREN BUFFET TABLE: ---------")
        print(results)
        # Convert query results into a DataFrame
        df = pd.DataFrame.from_records(results)
        if df.empty:
            return {}, []  # Return empty data if no records found

        # Sort DataFrame by Year (Descending) and then by Metric
        df.sort_values(
            by=["TimePeriodID__Year", "MetricID__MetricName"],
            ascending=[False, True],
            inplace=True,
        )

        # Transform data into a nested dictionary format
        metric_data = {
            metric: {
                str(row["TimePeriodID__Year"]): {
                    "value": row["Value"],
                    "class": f"valuation-{row['Valuation']}",
                }
                for _, row in group.iterrows()
            }
            for metric, group in df.groupby("MetricID__MetricName")
        }

        unique_years = sorted(df["TimePeriodID__Year"].unique(), reverse=True)
        print(unique_years)
        return metric_data, unique_years

    except Company.DoesNotExist:
        return f"Company with ticker '{ticker}' does not exist.", []
    except Exception as e:
        return f"An error occurred: {str(e)}", []


def fetch_data_from_db(ticker):
    try:
        company = Company.objects.get(Ticker=ticker)
        financial_data = FinancialData.objects.filter(CompanyID=company).select_related(
            "StatementTypeID", "MetricID", "TimePeriodID"
        )

        data = [
            {
                "Company": company.Name,
                "StatementType": entry.StatementTypeID.StatementName,
                "Metric": entry.MetricID.MetricName,
                "Year": entry.TimePeriodID.Year,
                "Quarter": entry.TimePeriodID.Quarter,
                "StartDate": entry.TimePeriodID.StartDate,
                "EndDate": entry.TimePeriodID.EndDate,
                "Value": entry.Value,
            }
            for entry in financial_data
        ]

        return pd.DataFrame(data)
    except Company.DoesNotExist:
        return f"Company with name '{ticker}' does not exist."
    except Exception as e:
        return f"An error occurred: {str(e)}"


def fetch_metrics_wb():
    return Metric.objects.filter(MetricType="wb").all()

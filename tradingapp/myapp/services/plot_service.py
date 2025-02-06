import pandas as pd
import plotly.express as px
from myapp.services.financial_service import fetch_graph_data
from myapp.services.financial_service import fetch_metrics_wb


def generate_plot_data(ticker):
    metrics = fetch_metrics_wb()
    graphs = []

    for metric in metrics:
        graph_data = fetch_graph_data(ticker, metric.MetricName)
        fig = px.line(
            graph_data, x="calendarYear", y=metric.MetricName, title=metric.MetricName
        )
        graphs.append(fig.to_html(full_html=False))

    return graphs

from myapp.models.metrictooltip_model import MetricTooltip


def fetch_tooltips(metrics=None) -> dict:
    """
    fetches tooltips from database
    if metrics is none fetches all tooltips

    """
    # Query to get all tooltips along with the corresponding MetricName
    tooltips = MetricTooltip.objects.select_related("Metric").all()

    # Initialize an empty dictionary to store the results
    tooltip_dict = {}

    # Loop through and add the results to the dictionary
    for tooltip in tooltips:
        tooltip_dict[tooltip.Metric.MetricName] = tooltip.Tooltip
    print("TOOLTIP")
    print(tooltip_dict)

    return tooltip_dict

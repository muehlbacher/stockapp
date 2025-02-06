def fetch_tooltips(metrics=None) -> dict:
    """
    fetches tooltips from database
    if metrics is none fetches all tooltips

    """
    if metrics is None:
        pass

    return {
        "deprecationRatio": "This is the depraction ratio tooltip!",
        "revenue": "this is the revenue tooltip for the revenue stuff .. ",
    }

import json

from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from myapp.forms import SignupForm
from myapp.services.plot_service import generate_plot_data
from myapp.services.company_service import (
    search_companies,
)
from myapp.services.financial_service import (
    prepare_table_data,
    prepare_wb_table_data,
    prepare_table_data_selected_metrics,
    CompanyDoesNotExistError,
)


def dashboard(request, search_term=None):
    # search_term = request.GET.get("search_term", "")
    if search_term is None:
        ticker = "NVDA"

    else:
        ticker = search_term.upper()
    try:
        financial_table_data, unique_years = prepare_table_data_selected_metrics(ticker)
    except CompanyDoesNotExistError:
        return render(
            request,
            "myapp/dashboard.html",
            {
                "financial_table_data": None,
            },
        )
    if isinstance(financial_table_data, str):  # If it's an error message
        return render(request, "error.html", {"error_message": financial_table_data})

    graphs = generate_plot_data(ticker)
    wb_table_data, unique_years_wb = prepare_wb_table_data(ticker)

    metric_tooltip = {
        "deprecationRatio": "This is the depraction ratio tooltip!",
        "revenue": "this is the revenue tooltip for the revenue stuff .. ",
    }
    print("wb_data--------")
    print(wb_table_data)

    return render(
        request,
        "myapp/dashboard.html",
        {
            "financial_table_data": financial_table_data,
            "wb_table_data": wb_table_data,
            "unique_years_wb": unique_years_wb,
            "unique_years": unique_years,
            "company_name": ticker,
            "graphs": graphs,
            "search_term": search_term,
            "metric_tooltip": metric_tooltip,
        },
    )


def dashboard_search(request):
    if request.method == "POST":
        # Get the search term from the POST request
        search_term = request.POST.get("search")

        # Redirect to the dashboard with the search term in the URL
        return redirect(f"/dash/{search_term}/")

    # If the request is not POST, just show the dashboard without search term
    return render(request, "myapp/dashboard.html", {"search_term": ""})


def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "POST":
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Signup successful!")
            return redirect("plotly_graph")
    else:
        form = SignupForm()
    return render(request, "myapp/signup.html", {"form": form})


@csrf_exempt
def search_preview(request):
    if request.method == "POST":
        data = json.loads(request.body)
        query = data.get("query", "")
        results = search_companies(query) if query else []
        return JsonResponse({"results": results})

    return JsonResponse({"results": []})

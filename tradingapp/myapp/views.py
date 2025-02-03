from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .forms import SignupForm
from .services.plot_service import generate_plot_data
from .services.company_service import fetch_companies_name_and_ticker, search_companies
from .services.financial_service import (
    fetch_data_from_db,
    prepare_table_data,
    prepare_wb_table_data,
    fetch_metrics_wb,
)


def plotly_graph(request):
    ticker = "CSIQ"
    companies = fetch_companies_name_and_ticker()
    choices = [(company["Ticker"], company["Name"]) for company in companies]

    selected_option = request.POST.get("search") if request.method == "POST" else None
    if selected_option:
        ticker = selected_option

    df = fetch_data_from_db(ticker)
    financial_table_data, unique_years = prepare_table_data(ticker)

    if isinstance(financial_table_data, str):  # If it's an error message
        return render(request, "error.html", {"error_message": financial_table_data})

    graphs = generate_plot_data(ticker)
    wb_table_data, unique_years_wb = prepare_wb_table_data(ticker)

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
        },
    )


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

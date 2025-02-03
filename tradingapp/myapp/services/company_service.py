from ..models.company_model import Company
from django.db.models import Q


def fetch_companies_name_and_ticker():
    return list(Company.objects.values("Ticker", "Name"))


def search_companies(query):
    results = Company.objects.filter(
        Q(Ticker__icontains=query) | Q(Name__icontains=query)
    )[:10]
    return [
        {"id": company.CompanyID, "name": company.Name, "ticker": company.Ticker}
        for company in results
    ]

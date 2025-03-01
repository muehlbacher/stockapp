from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path("dash/<str:search_term>/", views.dashboard, name="dashboard_with_search"),
    path("dash/", views.dashboard_search, name="dashboard_search"),
    path(
        "login/",
        auth_views.LoginView.as_view(template_name="myapp/login.html"),
        name="login",
    ),
    path("signup/", views.signup, name="signup"),
    path("search-preview/", views.search_preview, name="search_preview"),
]

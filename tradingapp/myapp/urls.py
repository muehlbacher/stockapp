from django.urls import path
from . import views

urlpatterns = [
    path('plotly/', views.plotly_graph, name='plotl_graph'),
]
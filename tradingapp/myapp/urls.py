from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('plotly/', views.plotly_graph, name='plotly_graph'),
    path('login/', auth_views.LoginView.as_view(template_name='myapp/login.html'), name='login'),
    path('signup/', views.signup, name='signup'),

]
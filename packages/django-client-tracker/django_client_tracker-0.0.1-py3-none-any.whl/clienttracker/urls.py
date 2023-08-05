from django.urls import path
from . import views

app_name = 'clienttracker'

urlpatterns = [
    path('', views.ticker, name='ticker'),
]

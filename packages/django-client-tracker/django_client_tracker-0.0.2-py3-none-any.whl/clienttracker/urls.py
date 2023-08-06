from django.urls import path
from . import views

app_name = 'clienttracker'

urlpatterns = [
    path('frequency/', views.frequency, name='frequency'),
    path('', views.ticker, name='ticker'),
]

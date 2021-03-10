from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name="finance-index"),
    path('hi', views.hi, name="hi"),
]
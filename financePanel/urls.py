from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name="finance-index"),
    path('index', views.index, name="index"),
]
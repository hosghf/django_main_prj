from django.urls import path
from . import views

urlpatterns = [
    path('', views.test, name="finance-index"),
    path('index', views.index, name="index"),
    path('test', views.test, name="test"),
    path('stocks/create', views.stocksCreate, name="stocks.create"),
    path('stocks/<int:pk>/update', views.stocksUpdate, name="stocks.update"),
    path('stocks', views.stocksIndex, name="stocks.update"),

    path('excel-to-db', views.excelToDb, name="excelToDb")
]

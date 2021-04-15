from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="finance-index"),
    path('index', views.index, name="index"),
    path('stocks/create', views.stocksCreate, name="stocks.create"),
    path('stocks/<int:pk>/update', views.stocksUpdate, name="stocks.update"),
    path('stocks', views.stocksIndex, name="stocks.update"),

    path('excel-to-db', views.excelToDb, name="excelToDb"),

    path('candle', views.candle, name="candle"),
    path('candle2', views.candle2, name="candle2"),
    path('histogram', views.histogram, name="histogram"),

    path('getFinanceData', views.getFinanceData, name="yfinance")
]

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpRequest
from .models import stockPrice
from .forms import stockModelForm
from django.core.paginator import Paginator
import os
import csv
import yfinance as yf

# for cvs file
from django.conf import settings
from django.core.files.storage import default_storage

# Create your views here.

def index(request):
    return render(request, 'financePanel/index.html')

def stocksIndex(request):
    stocks = stockPrice.objects.all()
    paginator = Paginator(stocks, 10)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'stocks' : stocks,
        'page_obj': page_obj
    }
    return render(request, 'financePanel/stocks_index.html', context)

def stocksCreate(request):
    if request.method == 'POST':
        form = stockModelForm(request.POST)
        if(form.is_valid()):
            form.save()
            print('form is save')
            return redirect('/finance-admin/stocks/create')
        else: 
            print('noooooooooooooooooooooooooottt vaaaaaliiiiiiiid')
            context = { 'form': form }
            return render(request, 'financePanel/stocks_create.html', context)

    form = stockModelForm()
    context = {
        'form': form
    }
    return render(request, 'financePanel/stocks_create.html', context)

def stocksUpdate(request, pk):
    stock = stockPrice.objects.get(id=pk)
    
    if(request.method == 'POST'):
        form = stockModelForm(request.POST, instance=stock)
        if(form.is_valid()):
            form.save()
            print('form has updated')
            return redirect('/finance-admin/stocks/' + str(pk) + '/update')
        else:
            context = { 'form': form }
            return render(request, 'financePanel/stocks_update.html', context)

    form = stockModelForm(instance=stock)
    context = {
        'form': form,
        'stock' : stock 
    }
    return render(request, 'financePanel/stocks_update.html', context)


def excelToDb(request):
    if request.method == 'GET':
        print('this is settings: ' + str(settings.BASE_DIR))
        return render(request, "financePanel/excel_to_db.html")
    
    csvFile = request.FILES['mfile']
    path = os.path.join(settings.BASE_DIR, 'tmp')
    
    if not os.path.isdir(path):
        os.mkdir(path, mode = 0o777)
        
    path = default_storage.save(path + '/' + str(csvFile) , csvFile)

    with open(path) as f:
        reader = csv.reader(f)
        next(f)
        for row in reader:
            print(row)
            created = stockPrice.objects.get_or_create(
                name=row[0],
                symbol=row[1],
                market=row[2],
                stok_type=row[3],
                size=row[4],
                open=row[5],
                date=row[6],
                low=row[7],
                high=row[8],
                close_price=row[9],
                volume=row[10],
                )

    default_storage.delete(path)
    
    return render(request, "financePanel/excel_to_db.html")


def getFinanceData(request):
    if request.method == "POST":
        symbol = request.POST['symbol']
        symbolTicker = yf.Ticker(symbol)
        # history = symbol.history(period='5d')
        dateFrom = request.POST['dateFrom']
        dateTo = request.POST['dateTo']
        history = symbolTicker.history(start=dateFrom, end=dateTo)
        if not history.index.empty:
            print('im not empty hahaha')

            for index, row in history.iterrows():
                created = stockPrice.objects.get_or_create(
                    date=str(index),
                    symbol= symbolTicker.info['symbol'],
                    defaults={
                        'name': symbolTicker.info['shortName'],
                        'market': symbolTicker.info['market'],
                        'high': str(row['High']),
                        'low': str(row['Low']),
                        'size': str(row['Volume']),
                        'open': str(row['Open']),     
                        'close_price': str(row['Close']),     
                        'volume': str(row['Volume']),  
                    },
                )
            message = "database is updated"
            context = { 'message': message }
            return render(request,'financePanel/yfinance.html', context)
    
    return render(request, 'financePanel/yfinance.html')

def candle(request):
    return render(request, 'financePanel/candle.html')

def candle2(request):

    low = []
    close = []
    high = []
    open = []
    date = []
    message = ''
    found = False
    post = False

    if request.method == 'POST':
        symbol = request.POST['symbol']
        dateFrom = request.POST['dateFrom']
        dateTo = request.POST['dateTo']
        stock = False

        if(dateFrom and dateTo):
            stock = stockPrice.objects.filter(symbol=symbol, date__range=(dateFrom, dateTo))

        if(stock):
            for rec in stock:
                low.append(str(rec.low))
                close.append(str(rec.close_price))
                high.append(str(rec.high))
                open.append(str(rec.open))
                date.append(str(rec.date))

        post = True
        if stock:
            found = True
            message = "your symbol not found in database, you can update database with your symbol"

    context = {
        'low': low,
        'close': close,
        'high': high,
        'open': open,
        'date': date,
        'found': found,
        'message': message,
        'post': post
    }
    return render(request, 'financePanel/candle2.html', context)
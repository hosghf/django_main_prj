from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.http import HttpRequest
from .models import stockPrice
from .forms import stockModelForm
from django.core.paginator import Paginator

# Create your views here.

def index(request):
    return render(request, 'financePanel/index.html')

def test(request):
    test2 = stockPrice.objects.get(low='10')
    # test2 = stockPrice.objects.all()
    # context = {'test2': test2, 'stock': stock}
    return render(request, 'financePanel/test.html', {'test2': test2})

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

from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def test(request):
    return HttpResponse('heellooooo')

def index(request):
    return render(request, 'financePanel/index.html')
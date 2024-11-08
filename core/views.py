from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "core/index.html")

def home(request):
    return render(request, 'core/home.html')

def product(request):
    return render(request, 'core/product.html')

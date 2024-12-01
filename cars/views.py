from django.shortcuts import render
from cars.models import Auto

def index_page(request):

    all_cars = Auto.objects.all ()

    print (all_cars)
    return render(request, 'index.html')

from .models import Auto

def index(request):
    autos = Auto.objects.all().order_by('-created_at')[:10]
    return render(request, 'index.html', {'autos': autos})
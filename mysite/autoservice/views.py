from django.shortcuts import render
from django.http import HttpResponse
from . models import Service, Order, Vehicle

# Create your views here.
def index(request):
    num_service = Service.objects.all().count()
    num_order = Order.objects.all().count()
    num_vehicle = Vehicle.objects.all().count()

    context = {
        'num_service': num_service,
        'num_order': num_order,
        'num_vehicle': num_vehicle
    }

    return render(request, 'index.html', context=context)

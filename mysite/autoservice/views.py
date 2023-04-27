from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from . models import Service, Order, Vehicle
from django.views import generic

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

def vehicles(request):
    vehicles = Vehicle.objects.all()
    context = {
        'vehicles': vehicles,
    }
    return render(request, 'vehicles.html', context=context)

def vehicle(request, vehicle_id):
    vehicle = get_object_or_404(Vehicle, pk=vehicle_id)
    context = {
        'vehicle': vehicle,
    }
    return render(request, 'vehicle.html', context=context)

class OrderListView(generic.ListView):
    model = Order
    context_object_name = "orders"
    template_name = "orders.html"


class OrderDetailView(generic.DetailView):
    model = Order
    context_object_name = "orders"
    template_name = "order.html"


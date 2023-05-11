from django.shortcuts import render, get_object_or_404, reverse
from django.http import HttpResponse
from .models import Service, Order, Vehicle, OrderLine
from django.views import generic
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.forms import User
from django.views.decorators.csrf import csrf_protect
from django.contrib import messages
from django.views.generic.edit import FormMixin
from .forms import OrderReviewForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm
from django.views.generic import (CreateView, UpdateView, DeleteView)
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import OrderCreateUpdateForm


# Create your views here.
def index(request):
    num_service = Service.objects.all().count()
    num_order = Order.objects.all().count()
    num_vehicle = Vehicle.objects.all().count()

    num_visits = request.session.get('num_visits', 1)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_service': num_service,
        'num_order': num_order,
        'num_vehicle': num_vehicle,
        'num_visits': num_visits,
    }

    return render(request, 'index.html', context=context)


def vehicles(request):
    paginator = Paginator(Vehicle.objects.all(), 2)
    page_number = request.GET.get('page')
    paged_vehicles = paginator.get_page(page_number)
    vehicles = paged_vehicles
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


def search(request):
    """
    paprasta paieška. query ima informaciją iš paieškos laukelio,
    search_results prafiltruoja pagal įvestą tekstą knygų pavadinimus ir aprašymus.
    Icontains nuo contains skiriasi tuo, kad icontains ignoruoja ar raidės
    didžiosios/mažosios.
    """
    query = request.GET.get('query')
    search_results = Vehicle.objects.filter(
        Q(owner_name__icontains=query) | Q(vehicle_model__make__icontains=query) | Q(
            vehicle_model__model__icontains=query) | Q(plate__icontains=query) | Q(vin__icontains=query))
    return render(request, 'search.html', {'vehicles': search_results, 'query': query})


class OrderListView(generic.ListView):
    model = Order
    paginate_by = 2
    context_object_name = "orders"
    template_name = "orders.html"


class OrderDetailView(LoginRequiredMixin, FormMixin, generic.DetailView):
    model = Order
    context_object_name = "order"
    template_name = "order.html"
    form_class = OrderReviewForm

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.object.id})

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order = self.object
        form.instance.reviewer = self.request.user
        form.save()
        return super(OrderDetailView, self).form_valid(form)


class ClientOrdersListView(LoginRequiredMixin, generic.ListView):
    model = Order
    template_name = "my_orders.html"
    context_object_name = "orders"

    def get_queryset(self):
        return Order.objects.filter(client=self.request.user).order_by('due_back')


class OrderCreateView(LoginRequiredMixin, CreateView):
    model = Order
    # fields = ['vehicle', 'due_back']
    success_url = "/autoservice/my_orders/"
    template_name = 'my_order_form.html'
    form_class = OrderCreateUpdateForm

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Order
    # fields = ['vehicle', 'due_back']
    success_url = "/autoservice/my_orders/"
    template_name = 'my_order_form.html'
    form_class = OrderCreateUpdateForm

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client


class OrderDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Order
    success_url = "/autoservice/my_orders/"
    template_name = 'my_order_delete.html'

    def test_func(self):
        order = self.get_object()
        return self.request.user == order.client


class OrderLineCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = 'my_orderline_form.html'

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['pk']})
    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['pk'])
        return super().form_valid(form)

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['pk'])
        return self.request.user == order.client


class OrderLineUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = OrderLine
    fields = ['service', 'quantity']
    template_name = 'my_orderline_form.html'

    def form_valid(self, form):
        form.instance.order = Order.objects.get(pk=self.kwargs['order_id'])
        return super().form_valid(form)

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        return self.request.user == order.client

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['order_id']})


class OrderLineDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = OrderLine
    template_name = 'my_orderline_delete.html'
    context_object_name = 'orderline'

    def test_func(self):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        return self.request.user == order.client

    def get_success_url(self):
        return reverse('order', kwargs={'pk': self.kwargs['order_id']})


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, f"Profilis atnaujintas")
            return redirect('profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'profile.html', context)

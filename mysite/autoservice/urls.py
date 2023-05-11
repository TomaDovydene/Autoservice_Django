from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('vehicles/', views.vehicles, name='vehicles'),
    path('vehicles/<int:vehicle_id>', views.vehicle, name='vehicle'),
    path('orders/', views.OrderListView.as_view(), name='orders'),
    path('orders/<int:pk>', views.OrderDetailView.as_view(), name='order'),
    path('search/', views.search, name='search'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('my_orders/', views.ClientOrdersListView.as_view(), name='my_orders'),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('my_orders/new', views.OrderCreateView.as_view(), name='my_new_order'),
    path('my_orders/<int:pk>/update', views.OrderUpdateView.as_view(), name='my_order_update'),
    path('my_orders/<int:pk>/delete', views.OrderDeleteView.as_view(), name='my_order_delete'),
    path("orders/<int:pk>/createline", views.OrderLineCreateView.as_view(), name="order_createline"),
    path("orders/<int:order_id>/updateline/<int:pk>", views.OrderLineUpdateView.as_view(), name="order_updateline"),
    path("orders/<int:order_id>/deleteline/<int:pk>", views.OrderLineDeleteView.as_view(), name="order_deleteline"),
]
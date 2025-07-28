from django.urls import path, reverse
from django.shortcuts import redirect
from . import views

app_name = 'orders'

urlpatterns = [
    path('create/', views.create_order, name='create_order'),
    path('<int:order_id>/', views.order_detail, name='order_detail'),
    path('', lambda request: redirect(reverse('orders:create_order'))),
]

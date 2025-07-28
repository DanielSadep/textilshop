from django.urls import path
from . import views

app_name = 'cart'

urlpatterns = [
    path('', views.cart_detail, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
]
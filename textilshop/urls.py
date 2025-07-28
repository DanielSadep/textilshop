from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),

    # Primero usuarios (autenticación base del sitio)
    path('users/', include('apps.users.urls')),

    # Luego las demás funcionalidades
    path('products/', include('apps.products.urls')),
    path('cart/', include('apps.cart.urls')),
    path('orders/', include('apps.orders.urls')),
    path('api/', include('apps.products.api.urls')),
    

    # Ruta raíz: redirige a login de usuarios
    path('', lambda request: redirect('users:login')),
]

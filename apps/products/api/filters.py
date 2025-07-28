from django_filters import rest_framework as filters
from django.db import models
from apps.products.models import Product

class ProductFilter(filters.FilterSet):
    sizes = filters.CharFilter(field_name='sizes', lookup_expr='icontains')
    colors = filters.CharFilter(field_name='colors', lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['category', 'sizes', 'colors']

        filter_overrides = {
            models.JSONField: {
                'filter_class': filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
        }

from django.db import models
from apps.products.models import Product

class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    session_key = models.CharField(max_length=40)  # Para manejar carritos sin login

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

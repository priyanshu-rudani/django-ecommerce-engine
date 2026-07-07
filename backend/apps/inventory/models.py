from django.db import models
from apps.core.models import BaseModel

from datetime import timedelta
from django.utils import timezone


def reservation_expiry():
    return timezone.now() + timedelta(minutes=10)


# Create your models here.
class packages(BaseModel):
    package_name = models.CharField(max_length=255)
    packaging_charges = models.DecimalField(max_digits=10, decimal_places=2)
    container_type = models.CharField(
        max_length=100, 
        choices=[
            ('box', 'Box'), 
            ('bag', 'Bag'), 
            ('envelope', 'Envelope'), 
            ('other', 'Other')
        ])
    length = models.DecimalField(max_digits=10, decimal_places=2)
    breadth = models.DecimalField(max_digits=10, decimal_places=2)
    height = models.DecimalField(max_digits=10, decimal_places=2)
    dimension_unit = models.CharField(
        max_length=100, 
        choices=[
            ('cm', 'Centimeters'), 
            ('m', 'Meters'), 
            ('in', 'Inches'), 
            ('ft', 'Feet')
            ])
    weight = models.DecimalField(max_digits=10, decimal_places=2)
    weight_unit = models.CharField(
        max_length=100, 
        choices=[
            ('kg', 'Kilograms'), 
            ('g', 'Grams'), 
            ('lb', 'Pounds'), 
            ('oz', 'Ounces')
            ])
    


class inventory(BaseModel):
    variant = models.OneToOneField('catalog.product_variants', on_delete=models.CASCADE, related_name='inventory')
    total_quantity = models.PositiveIntegerField(default=0)
    reserved_quantity =  models.PositiveIntegerField(default=0)
    low_stock_threshold = models.PositiveIntegerField(default=0)

    @property
    def available_quantity(self):
        return self.total_quantity - self.reserved_quantity


class inventory_reservation(BaseModel):
    user_id = models.ForeignKey('identity.user_profiles', on_delete=models.SET_NULL, null=True, blank=True, related_name='inventory_reservation')
    cart_id = models.ForeignKey('checkout.shopping_carts', on_delete=models.SET_NULL, null=True, blank=True,  related_name='inventory_reservation')
    variant = models.ForeignKey('catalog.product_variants', on_delete=models.SET_NULL, null=True, blank=True,  related_name='inventory_reservation')
    quantity = models.PositiveIntegerField(default=0)
    expires_at = models.DateTimeField(default=reservation_expiry)
    status = models.CharField(
        max_length=30, 
        choices=[
            ('active', 'Active'),
            ('confirmed', 'Confirmed'),
            ('expired', 'Expired'),
            ('cancelled', 'Cancelled'),
        ],
        default="active",
    )



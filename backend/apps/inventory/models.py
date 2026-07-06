from django.db import models
from apps.core.models import BaseModel
from apps.identity.models import user_profiles


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
    

# bug: Redesign these with AI inline suggestion: 

class inventory_lock(BaseModel):
    variant = models.ForeignKey('inventory.variants', on_delete=models.CASCADE, related_name='inventory_lock')
    available_quantity = models.IntegerField(default=0)
    reserved_quantity =  models.IntegerField(default=0)
    low_stock_threshold = models.IntegerField(default=0)
    expires_at = models.TimeField()
    status = models.CharField(max_length=30, choices=[])


class inventory_items(BaseModel):
    user_id = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='inventory_items')
    # cart_id = models.ForeignKey('', on_delete=models.CASCADE, related_name='inventory_items')
    # variant_id = models.ForeignKey('', on_delete=models.CASCADE, related_name='inventory_items')
    quantity = models.IntegerField(default=0)
    expires_at = models.TimeField()
    status = models.CharField(max_length=30, choices=[])

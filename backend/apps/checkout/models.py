from django.db import models
from apps.core.models import BaseModel
from apps.identity.models import user_profiles
from apps.catalog.models import product_variants

# Create your models here.
class shopping_carts(BaseModel):
    session_token = models.CharField(max_length=256, null=True, blank=True)
    user = models.ForeignKey(
        user_profiles,
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='carts'
    )


class shopping_carts_items(BaseModel):
    cart_id = models.ForeignKey(shopping_carts, on_delete=models.CASCADE, related_name="carts_items")
    variant_id = models.ForeignKey(product_variants, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)


class orders(BaseModel):
    order_number = models.CharField(max_length=20)
    order_date = models.DateField(auto_now_add=True)
    order_status = models.CharField(
        max_length=50, 
        choices=[
            ('waiting_for_payment', 'Waiting for payment'),
            ('placed', 'Order Confirmed'),
            ('cancelled', 'cancelled'),
            ('picked_up', 'Order Picked up'),
            ('in_transit', 'Order in Transit'),
            ('out_for_delivery', 'Out for delivery'),
            ('delivered', 'Delivered'),
            ('attempted_delivery', 'Attempted delivery'),
            ('return', 'Return (RTO)')
        ]
    )
    payment_method = models.CharField(
        max_length=50, 
        choices=[
            ('cash_on_delivery', 'Cash on delivery (COD)'),
            ('pre_paid', 'Pre Paid'),
            ('partially_paid', 'Partially Paid'),
            ('refunded', 'Refunded'),
        ]
    )
    user_id = models.ForeignKey(user_profiles, on_delete=models.CASCADE)
    items_subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    order_discount  = models.DecimalField(max_digits=10, decimal_places=2)
    is_international = models.BooleanField(default=False)
    shipping_snapshot = models.JSONField()
    shipping_charges  = models.DecimalField(max_digits=10, decimal_places=2)
    tax_amount  = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount  = models.DecimalField(max_digits=10, decimal_places=2)
    other_charges  = models.DecimalField(max_digits=10, decimal_places=2)
    idempotency_token = models.CharField(max_length=100, unique=True)
    courier_name = models.CharField(max_length=50) 
    courier_id = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50, unique=True)
    is_deleted = models.BooleanField(default=False)


class order_items(BaseModel):
    order_id = models.ForeignKey(orders, on_delete=models.CASCADE, related_name='order_items')
    variant_id = models.ForeignKey(product_variants, on_delete=models.CASCADE, related_name='order_items')
    item_image_id = models.CharField(max_length=20)
    item_name = models.CharField(max_length=50)
    item_sku = models.CharField(max_length=20)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    item_total = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.CharField(max_length=15)
    tax_rate = models.CharField(max_length=10)
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2)


class payment_transactions(BaseModel):
    order_id = models.ForeignKey(orders, on_delete=models.SET_NULL)
    user_id = models.ForeignKey(user_profiles, on_delete=models.CASCADE)
    gateway_provider = models.CharField()
    gateway_transaction_id = models.CharField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(
        max_length=50,
        choices=[
            ('card','card'),
            ('netbanking','netbanking'),
            ('wallet','wallet'),
            ('emi','emi'),
            ('upi','upi'),
            ('other', 'other'),
        ]
    )
    payment_status = models.CharField(
        max_length=50,
        choices=[
            ('created','created'),
            ('authorized','authorized'),
            ('captured','captured'),
            ('refunded','refunded'),
            ('failed','failed'),
            ('canceled', 'canceled'),
        ]
    )
    cryptographic_signature = models.CharField()
    is_deleted = models.BooleanField(default=False) 


    
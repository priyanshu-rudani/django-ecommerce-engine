from django.db import models
from apps.core.models import BaseModel
from apps.inventory.models import user_profiles
from apps.checkout.models import orders
from apps.inventory.models import packages

# Create your models here.
class return_requests(BaseModel):
    return_number = models.CharField(max_length=20)
    user_id = models.ForeignKey(user_profiles, on_delete=models.CASCADE)
    order_id = models.ForeignKey(orders, on_delete=models.CASCADE)
    requested_method = models.CharField(
        max_length=50, 
        choices=[
            ('return', 'Return'),
            ('partial_return', 'Partial Return'),
            ('replacement', 'Replacement'),
            ('refund', 'Refund'),
        ])
    request_status = models.CharField(
        max_length=50, 
        choices=[
            ('requested', 'Requested'),
            ('processing', 'Processing'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('completed', 'Completed'),
        ])
    return_reason = models.CharField(max_length=80)
    settlement_methods = models.CharField(
        max_length=50, 
        choices=[
            ('return', 'Return'),
            ('partial_return', 'Partial Return'),
            ('replacement', 'Replacement'),
            ('refund', 'Refund'),
        ])
    settlement_date = models.DateField()
    transaction_reference = models.CharField(max_length=50)
    customer_paid = models.DecimalField(max_digits=10, decimal_places=2)
    eligible_refund = models.DecimalField(max_digits=10, decimal_places=2)

    refund_total = models.CharField(max_length=50)
    refund_transaction_id = models.CharField(max_length=50)
    is_deleted = models.BooleanField(default=False) 


class return_shipment(BaseModel):
    return_request_id = models.ForeignKey(return_requests, on_delete=models.CASCADE, related_name='shipments')
    shipping_carrier = models.CharField(max_length=50)
    tracking_number = models.CharField(max_length=50)
    label_url = models.CharField()
    label_created_at  = models.DateField()
    shipment_status = models.CharField(max_length=50)
    return_charges = models.DecimalField(max_digits=10, decimal_places=2)
    package_id = models.ForeignKey(packages, on_delete=models.SET_NULL, null=True, blank=True)


class return_items(BaseModel):
    return_request_id = models.ForeignKey(return_requests, on_delete=models.CASCADE, related_name='items')
    order_id = models.ForeignKey(orders, on_delete=models.CASCADE)
    variant_id = models.ForeignKey(orders, on_delete=models.CASCADE)
    item_quantity = models.IntegerField(max_length=10)
    item_condition = models.CharField(max_length=50)
    customer_proof_images = models.FileField(upload_to='/returns/user_uploads/')
    serial_number = models.CharField(max_length=80, blank=True, null=True)
    is_inspected = models.BooleanField(default=False)
    restockable = models.BooleanField(default=True)

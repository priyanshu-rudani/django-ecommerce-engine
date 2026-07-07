from django.db import models
from apps.core.models import BaseModel

# Create your models here.
class coupons(BaseModel):
    coupon_code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=[('percentage', 'Percentage'), ('fixed', 'Fixed Amount')])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    applies_to = models.CharField(
        max_length=100, 
        choices=[
            ('all_products', 'All Products'), 
            ('specific_products', 'Specific Products'),
            ('specific_categories', 'Specific Categories'),
            ('specific_users', 'Specific Users'),
            ('specific_user_groups', 'Specific User Groups'),
            ('specific_payment_methods', 'Specific Payment Methods'),
            ('specific_shipping_methods', 'Specific Shipping Methods')
            ])
    applicable_items = models.JSONField(null=True, blank=True)  # Store IDs of specific products, categories, users, etc.
    min_order_value = models.DecimalField(max_digits=10, decimal_places=2)
    max_discount_cap = models.DecimalField(max_digits=10, decimal_places=2)
    can_be_combined = models.BooleanField(default=False)
    usage_limit_total = models.IntegerField(null=True, blank=True)
    usage_limit_per_user = models.IntegerField(null=True, blank=True)
    current_usage_count = models.IntegerField(default=0)
    starts_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)



class coupon_redemptions(BaseModel):
    coupon_id = models.ForeignKey(coupons, on_delete=models.CASCADE, related_name='redemptions')
    user_id = models.ForeignKey('identity.user_profiles', on_delete=models.CASCADE, related_name='coupon_redemptions')
    order_id = models.CharField(max_length=100, null=True, blank=True) 
    discount_retained = models.DecimalField(max_digits=10, decimal_places=2)
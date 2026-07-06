from django.db import models
from autoslug import AutoSlugField
from apps.identity.models import user_profiles
from apps.inventory.models import packages
from apps.core.models import BaseModel, media_assets

# Create your models here.
class categories(BaseModel):
    parent_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True, always_update=True)   
    description = models.TextField()
    image = models.ImageField(upload_to='category_images/', null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name
    

class products(BaseModel):

    product_title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='product_title', unique=True, always_update=True)
    product_description = models.TextField()
    category_id = models.ForeignKey(categories, on_delete=models.CASCADE, related_name='products')
    style_code = models.CharField(max_length=100)
    group_id = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    listing_status = models.CharField(
        max_length=100, 
        choices=[
            ('draft', 'Draft'), 
            ('published', 'Published'), 
            ('archived', 'Archived')
            ])
    product_mrp = models.DecimalField(max_digits=10, decimal_places=2)
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    hsn_code = models.CharField(max_length=100)
    search_keywords = models.TextField()
    attributes = models.JSONField(default=dict)

    def __str__(self):
        return self.product_title
    

class product_variants(BaseModel):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, related_name='variants')
    variant_title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='variant_title', unique=True, always_update=True)
    sku = models.CharField(max_length=100, unique=True)
    serial_number = models.CharField(max_length=80, blank=True, null=True)
    variant_price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_status = models.CharField(
        max_length=100, 
        choices=[
            ('in_stock', 'In Stock'), 
            ('out_of_stock', 'Out of Stock'), 
            ('pre_order', 'Pre Order')
            ])
    package_id = models.ForeignKey(packages, on_delete=models.CASCADE, null=True, blank=True, related_name='product_variants')
    is_active = models.BooleanField(default=True)
    attributes = models.JSONField(default=dict)

    def save(self, *args, **kwargs):
        # If no price was provided, pull it from the parent product
        if not self.variant_price:
            self.variant_price = self.products.base_price
        super().save(*args, **kwargs)
    

    def __str__(self):
        return self.variant_title
    
class product_images(BaseModel):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, related_name='images')
    variant_id = models.ForeignKey(product_variants, on_delete=models.CASCADE, null=True, blank=True, related_name='images')
    media_asset_id = models.ForeignKey(media_assets, on_delete=models.CASCADE, related_name='product_images')
    is_primary = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)
    is_primary = models.BooleanField(default=False)


    class Meta:
        ordering = ['sort_order']

    def __str__(self):
        if self.variant_id:
            return f"Image for {self.variant_id.variant_title}"
        return f"Image for {self.product_id.product_title}"
    

class product_attributes(BaseModel):
    display_label = models.CharField(max_length=100)
    input_type = models.CharField(max_length=100, choices=[
        ('text', 'Text'),
        ('number', 'Number'),
        ('alphanumeric', 'Alphanumeric'),
        ('colour', 'Color'),  
    ])
    attribute_name = models.CharField(max_length=100)
    attribute_value = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.display_label}"
    

class product_reviews(BaseModel):
    product_id = models.ForeignKey(products, on_delete=models.CASCADE, related_name='reviews')
    customer_id = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='reviews')

    # todo: Add order_item_id to link the review to a specific order item
    # order_item_id = models.ForeignKey('orders.order_items', on_delete=models.CASCADE, related_name='reviews')

    rating = models.PositiveIntegerField()
    review_text = models.TextField()
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return f"Review by {self.customer_id.email} for {self.product_id.product_title}"
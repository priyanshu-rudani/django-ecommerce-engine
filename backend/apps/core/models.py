import string
import random

from django.db import models


def generate_id(length=8):
    """Generates a random numeric string of specified length."""
    return ''.join(random.choices(string.digits, k=length))



class BaseModel(models.Model):
    """
    An abstract base class model that provides self-updating
    'created_at' and 'updated_at' fields and automatic id Generating 
    """
    id = models.CharField(primary_key=True, default=generate_id, max_length=16, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True) 

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if not self.id:
            # Generate a unique ID
            self.id = generate_id(8)
            # Check if this ID already exists in the table
            # Since this is an abstract model, 'self.__class__' refers to the actual child model
            while self.__class__.objects.filter(id=self.id).exists():
                self.id = generate_id(8)
        
        super().save(*args, **kwargs)


class media_assets(BaseModel):
    """
    Model to store media assets information.
    """
    file_path = models.FileField(upload_to='library/')
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=60)
    file_size = models.PositiveIntegerField()  # Size in bytes
    width = models.PositiveIntegerField(null=True, blank=True)
    height = models.PositiveIntegerField(null=True, blank=True)
    alt_text = models.CharField(max_length=255, blank=True, null=True)
    is_deleted = models.BooleanField(default=False)


class global_configs(models.Model):
    """
    These store global configuration data about the website.
    Like: store name, tagline, description etc.
    """
    id = models.AutoField(primary_key=True, )
    config_key = models.CharField(max_length=500, blank=True, null=True)
    config_value = models.CharField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)

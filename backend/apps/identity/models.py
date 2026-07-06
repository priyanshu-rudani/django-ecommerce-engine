from django.db import models
from apps.core.models import BaseModel


# User Profiles Model 
class user_profiles(BaseModel):
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    first_name = models.CharField(max_length=40, blank=True)
    last_name = models.CharField(max_length=40, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    auth_provider = models.CharField(max_length=50, blank=True, null=True)
    auth_provider_uid = models.CharField(max_length=255, blank=True, null=True)
    is_gstin = models.BooleanField(default=False)
    gstin = models.CharField(max_length=15, blank=True, null=True)
    last_login_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)



class user_address(BaseModel):
    user = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='addresses')
    recipient_name = models.CharField(max_length=100)
    contact_phone = models.CharField(max_length=15)
    address_type = models.CharField(
        max_length=50, 
        choices=[
            ('home', 'Home'), 
            ('work', 'Work'), 
            ('other', 'Other')
        ])
    is_default = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=255)
    address_line2 = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)

    

class refresh_tokens(BaseModel):
    user = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='refresh_tokens')
    token_hash = models.CharField(max_length=255, unique=True)
    device_info = models.CharField(max_length=255, blank=True, null=True)
    is_revoked = models.BooleanField(default=False)
    expires_at = models.DateTimeField()


    
class user_otp_verifications(BaseModel):
    user = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='otp_verifications')
    identifier = models.CharField(max_length=255)  # This can be email or phone number
    otp_hash = models.CharField(max_length=6)
    purpose = models.CharField(
        max_length=50, 
        choices=[
            ('email_verification', 'Email Verification'), 
            ('phone_verification', 'Phone Verification')
        ])
    attempt_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    expires_at = models.DateTimeField()

    

class security_login_logs(BaseModel):
    user = models.ForeignKey(user_profiles, on_delete=models.CASCADE, related_name='login_logs')
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    attempted_email = models.EmailField(blank=True, null=True)
    failure_reason = models.CharField(max_length=255, blank=True, null=True)
    successful = models.BooleanField(default=False)

    

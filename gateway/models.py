from django.db import models
from user.models import User
from django.core.validators import RegexValidator

class Gateway(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='gateways')
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='gateway_photos/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    auto_select_assets = models.BooleanField(default=False)
    assets = models.ManyToManyField('assets.Asset', related_name='gateways', blank=True)
    website_url = models.URLField(unique=True, blank=False, null=False)
    support_email = models.EmailField(blank=False, null=False)
    support_link = models.URLField(validators= [RegexValidator(
        regex=r'^(?:https?://)?(?:www\.)?[A-Za-z0-9.-]+\.[A-Za-z]{2,}(?:/(?:[^/\s]+(?:/[^/\s]*)*))?$',
        message="Enter a valid URL."
    )], max_length=200, blank=False, null=False)
    phone_number = models.CharField(max_length=20, blank=True, null=True)

    TRANSACTION_PAYER_CHOICES = [
        ('merchant', 'Merchant'),
        ('user', 'User'), 
        ]
    
    transaction_fee_payer = models.CharField(
        max_length=10,
        choices=TRANSACTION_PAYER_CHOICES,
        default='merchant'
    )

    commission_fee_payer = models.CharField(
        max_length=10,
        choices=TRANSACTION_PAYER_CHOICES,
        default='merchant'
    )

    COVER_TYPE_CHOICES = [
        ('usd', 'USD'),
        ('percentage', 'Percentage'), 
        ]
    
    cover_type = models.CharField(
        max_length=10,  
        choices=COVER_TYPE_CHOICES,
        default='usd'
    )

    cover_range_up = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cover_range_down = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    


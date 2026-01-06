from django.db import models
from gateway.models import Gateway
from assets.models import Asset, Network, AssetNetwork

class CurrencyChoices(models.TextChoices):
        USD = 'USD', 'US Dollar'
        EUR = 'EUR', 'Euro'
        GBP = 'GBP', 'British Pound'
        AED = 'AED', 'United Arab Emirates Dirham'
        IRT = 'IRT', 'Iranian Rial'
        TRY = 'TRY', 'Turkish Lira'


class Paylink(models.Model):

    TRANSACTION_PAYER_CHOICES = [
        ('merchant', 'Merchant'),
        ('user', 'User'), 
    ]

    COVER_TYPE_CHOICES = [
        ('usd', 'USD'),
        ('percentage', 'Percentage'), 
    ]
        

    product_name = models.CharField(max_length=100)
    product_description = models.TextField(blank=True, null=True)
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='paylinks')
    instagram_link = models.URLField(max_length=200, blank=True, null=True)
    telegram_link = models.URLField(max_length=200, blank=True, null=True)
    assets = models.ManyToManyField(Asset, related_name='paylinks')
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateField(blank=True, null=True)
    payment_amount = models.DecimalField(max_digits=20, decimal_places=8, blank=True, null=True)
    is_amount_user_selectable = models.BooleanField(default=False)
    limited_uses = models.PositiveIntegerField(blank=True, null=True) #if not set, unlimited uses
    transaction_fee_payer = models.CharField(
        max_length=10,
        choices=TRANSACTION_PAYER_CHOICES,
        default='merchant'
    )
    transaction_commission_fee_payer = models.CharField(
        max_length=10,
        choices=TRANSACTION_PAYER_CHOICES,
        default='merchant'
    )
    cover_type = models.CharField(
        max_length=10,  
        choices=COVER_TYPE_CHOICES,
        default='usd'
    )
    cover_range_up = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    cover_range_down = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, null=True, blank=True)
    is_on = models.BooleanField(default=True)
    code = models.CharField(max_length=64, unique=True, blank=True, null=True)
    currency = models.CharField(
        max_length=3,
        choices=CurrencyChoices.choices,
        default=CurrencyChoices.USD
    )




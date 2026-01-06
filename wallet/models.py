from django.db import models
from gateway.models import Gateway
from assets.models import Asset, Network, AssetNetwork


class Wallet(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='wallets')
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='wallets')
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.network.symbol} ({self.gateway.name})"
    
    class Meta:
        unique_together = ('gateway', 'network', 'address')
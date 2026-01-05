from django.db import models
from assets.models import Asset, Network, AssetNetwork
from gateway.models import Gateway


class Transaction(models.Model):
    STATUS_CHOICES = [
        ('in progress', 'In Progress'),
        ('success', 'Success'),
        ('expired', 'Expired'),
        ('acceptable', 'Acceptable'),
        ('mismatch' , 'Mismatch'),
    ]

    TYPE_CHOICES = [
        ('direct', 'Direct'), 
        ('paylink', 'Paylink'),
    ]

    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='transactions')
    asset_network = models.ForeignKey(AssetNetwork, on_delete=models.CASCADE, related_name='transactions')
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='transactions')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in progress')
    payment_UID = models.CharField(max_length=100, unique=True, blank=False, null=False)
    details = models.TextField(blank=True, null=True)
    transaction_hash = models.CharField(max_length=200, blank=True, null=True, unique=True)


    def __str__(self):
        return f"Transaction {self.id} - {self.asset.symbol} via {self.gateway.name}"

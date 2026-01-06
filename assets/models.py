from django.db import models

class Network(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"
    

class Asset(models.Model):
    name = models.CharField(max_length=100, unique=True)
    symbol = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return f"{self.name} ({self.symbol})"

class AssetNetwork(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='asset_networks')
    network = models.ForeignKey(Network, on_delete=models.CASCADE, related_name='network_assets')
    price_usd = models.DecimalField(max_digits=20, decimal_places=8)
    transaction_fee = models.DecimalField(max_digits=10, decimal_places=4)

    class Meta:
        unique_together = ('asset', 'network')

    def __str__(self):
        return f"{self.asset.name} on {self.network.name}"
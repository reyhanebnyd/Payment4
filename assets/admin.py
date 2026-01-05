from django.contrib import admin
from .models import Asset, Network, AssetNetwork

@admin.register(Network)
class NetworkAdmin(admin.ModelAdmin):
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):    
    list_display = ('name', 'symbol')
    search_fields = ('name', 'symbol')

@admin.register(AssetNetwork)
class AssetNetworkAdmin(admin.ModelAdmin):
    list_display = ('asset', 'network', 'price_usd', 'transaction_fee')
    list_filter = ('network', 'asset')
    search_fields = ('asset__name', 'network__name')




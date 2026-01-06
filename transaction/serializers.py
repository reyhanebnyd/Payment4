from .models import Transaction
from assets.models import Asset, Network, AssetNetwork
from gateway.models import Gateway
from rest_framework import serializers

class TransactionSerializer(serializers.ModelSerializer):
    asset_name = serializers.CharField(source='asset.name', read_only=True)
    asset_symbol = serializers.CharField(source='asset.symbol', read_only=True)
    network_name = serializers.CharField(source='asset_network.network.name', read_only=True)
    network_symbol = serializers.CharField(source='asset_network.network.symbol', read_only=True)
    gateway_name = serializers.CharField(source='gateway.name', read_only=True)
    payed = serializers.BooleanField

    class Meta:
        model = Transaction
        fields = [
            'id',
            'gateway',
            'gateway_name',
            'asset',
            'asset_name',
            'asset_symbol',
            'network_name',
            'network_symbol',
            'asset_network',
            'amount',
            'created_at',
            'status',
            'payment_UID',
            'details',
            'transaction_hash',
            'type',
            'paylink',
        ]


class MockPaymentSerializer(serializers.Serializer):
    paid_amount = serializers.DecimalField(max_digits=20, decimal_places=8)
    transaction_hash = serializers.CharField(required=False, allow_blank=True)        

    class Meta:
        model = Transaction
        fields = [
            'paid_amount',
            'transaction_hash',
        ]
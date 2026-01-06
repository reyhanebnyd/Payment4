from rest_framework import serializers
from .models import Gateway, GatewayBalance
from assets.models import Asset

class GatewaySerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(
        many=True, required=False, queryset=Asset.objects.all()
    )
    class Meta:
        model = Gateway
        fields = ['id', 'name','photo', 'assets', 'created_at', 'updated_at', 
                  'auto_select_assets', 'website_url', 'support_email', 'support_link', 
                  'phone_number', 'transaction_fee_payer', 'commission_fee_payer', 
                  'cover_type', 'cover_range_up', 'cover_range_down']

class GatewayBalanceSerializer(serializers.ModelSerializer):
    fiat_balance = serializers.SerializerMethodField()

    class Meta:
        model = GatewayBalance
        fields = ['asset', 'balance', 'fiat_balance']

    def get_fiat_balance(self, obj):
        return obj.balance * obj.asset.usd_price    

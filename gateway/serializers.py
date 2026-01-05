from rest_framework import serializers
from .models import Gateway
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


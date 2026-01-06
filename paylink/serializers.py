from django.utils import timezone
from rest_framework import serializers
from assets.models import Asset
from .utils import generate_unique_code
from .models import Paylink

class PayLinkSerializer(serializers.ModelSerializer):
    assets = serializers.PrimaryKeyRelatedField(queryset=Asset.objects.all(), many=True)

    paymenent_url = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Paylink
        exclude = ['gateway', 'code']

    def validate_expires_at(self, value):
        if value and value <= timezone.now().date():
            raise serializers.ValidationError("Expiration date must be in the future.")    


    def get_paymenent_url(self, obj):
            request = self.context.get('request')
            if request is not None:
                return request.build_absolute_uri(f'/paylink/pay/{obj.code}/')
            return f'/paylink/pay/{obj.code}/'
        
    def create(self, validated_data):
        assets_data = validated_data.pop('assets', [])
        paylink = Paylink.objects.create(gateway=self.context['gateway'],
                                         code = generate_unique_code(),
                                        **validated_data)
        paylink.assets.set(assets_data)
        return paylink
    
    def update(self, instance, validated_data):
        assets_data = validated_data.pop('assets', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        if assets_data is not None:
            instance.assets.set(assets_data)
        return instance
    

class PayLinkChekoutSerializer(serializers.ModelSerializer):
    name = serializers.CharField()
    mobile_number = serializers.CharField()
    email = serializers.EmailField()
    description = serializers.CharField(required=False, allow_blank=True)
    asset_id = serializers.IntegerField()
    network_id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=20, decimal_places=8, required=False)

    class Meta:
        model = Paylink
        fields = [
            'name',
            'mobile_number',
            'email',
            'description',
            'asset_id',
            'network_id',
            'amount',
        ]
from django.utils import timezone
from django.http import Http404
from django.shortcuts import render
from gateway.models import Gateway
from paylink.serializers import PayLinkSerializer, PayLinkChekoutSerializer
from transaction.models import Transaction
from rest_framework import generics, permissions
from .models import Paylink
from rest_framework import viewsets
from rest_framework.response import Response
from assets.models import Asset, Network, AssetNetwork
from transaction.utils import generate_unique_payment_uid
from django.db import transaction as db_transaction




class PayLinkViewSet(viewsets.ModelViewSet):
    serializer_class = PayLinkSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Paylink.objects.filter(gateway__user=self.request.user)

    def get_serializer_context(self):
        context =  super().get_serializer_context()
        context['gateway'] = Gateway.objects.get(user=self.request.user)
        return context
    
    
    


class PublicPaylinkView(generics.RetrieveAPIView):
    authentication_classes = []
    permission_classes = [permissions.AllowAny]    

    def get(self, request, code):
        try:
            paylink = Paylink.objects.select_related('gateway').prefetch_related('assets').get(code=code, is_on=True)
        except Paylink.DoesNotExist:
            raise Http404("Paylink not found or is inactive.")

        if paylink.expires_at and paylink.expires_at < timezone.now():
            return Response({"detail": "This paylink has expired."}, status=410)
        
        if paylink.limited_uses is not None:
            successful_transactions_count = Transaction.objects.filter(
                paylink=paylink,
                status='success'
            ).count()
            if successful_transactions_count >= paylink.limited_uses:
                return Response({"detail": "This paylink has reached its usage limit."}, status=410)
        
        
        return Response({
            "product_name": paylink.product_name,
            "product_description": paylink.product_description,
            "payment_amount": paylink.payment_amount,
            "is_amount_user_selectable": paylink.is_amount_user_selectable,
            "asset_networks": [
                {
                    "id": asset_network.id,
                    "name": asset_network.asset.name,
                    "symbol": asset_network.asset.symbol,
                    "network": asset_network.network.name,
                    "price_in_usd": asset_network.price_usd,
                    "transaction_fee": asset_network.transaction_fee,
                }
                for asset in paylink.assets.all()
                for asset_network in asset.asset_networks.all()
            ],
            "instagram_link": paylink.instagram_link,
            "telegram_link": paylink.telegram_link,
            "transaction_fee_payer": paylink.transaction_fee_payer,
            "transaction_commission_fee_payer": paylink.transaction_commission_fee_payer,
            "cover_type": paylink.cover_type,
            "cover_range_up": paylink.cover_range_up,
            "cover_range_down": paylink.cover_range_down,
        })


class PaylinkCheckoutView(generics.CreateAPIView):
    serializer_class = PayLinkChekoutSerializer
    authentication_classes = []
    permission_classes = [permissions.AllowAny]    

    def post(self, request, code):
        try:
            paylink = Paylink.objects.select_related('gateway').prefetch_related('assets').get(code=code, is_on=True)
        except Paylink.DoesNotExist:
            raise Http404("Paylink not found or is inactive.")

        if paylink.expires_at and paylink.expires_at < timezone.now():
            return Response({"detail": "This paylink has expired."}, status=410)
        
        if paylink.limited_uses is not None:
            successful_transactions_count = Transaction.objects.filter(
                paylink=paylink,
                status='success'
            ).count()
            if successful_transactions_count >= paylink.limited_uses:
                return Response({"detail": "This paylink has reached its usage limit."}, status=410)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        if paylink.is_amount_user_selectable:
            amount = data.get('amount')
            if amount is None:
                return Response({"detail": "Amount must be chosen by you"}, status=400)
            if amount <= 0:
                return Response({"detail": "Amount must be greater than zero."}, status=400)
            if paylink.cover_type == "USD":
                if paylink.cover_range_up and amount > paylink.cover_range_up:
                    return Response({"detail": f"Amount cannot exceed {paylink.cover_range_up} USD."}, status=400)
                if paylink.cover_range_down and amount < paylink.cover_range_down:
                    return Response({"detail": f"Amount cannot be less than {paylink.cover_range_down} USD."}, status=400)
                
        try:
            asset = paylink.assets.get(id=data['asset_id'])
        except Asset.DoesNotExist:
            return Response({"detail": "Selected asset is not available for this paylink."}, status=400)        

        try:
            asset_network = AssetNetwork.objects.get(network=data['network_id'], asset=data['asset_id'])
        except AssetNetwork.DoesNotExist:
            return Response({"detail": "Selected network is invalid for this asset."}, status=400)

        details = f"Paylink Checkout for {paylink.product_name} by {data['name']}, Email: {data['email']}, Mobile: {data['mobile_number']}"
        payment_UID = generate_unique_payment_uid()
        with db_transaction.atomic():
            transaction = Transaction.objects.create(   
                paylink=paylink,
                asset=asset,
                asset_network=asset_network,
                amount=data.get('amount', paylink.payment_amount),
                gateway=paylink.gateway,
                status='pending',
                type='paylink',
                details=details,
                payment_UID=payment_UID
            )
            paylink.save()
        return Response({
            "transaction_id": transaction.id,  
            "payment_UID": transaction.payment_UID,
            "status": transaction.status
        })
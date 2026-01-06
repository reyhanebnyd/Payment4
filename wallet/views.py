from django.shortcuts import render
from .models import Wallet
from rest_framework import viewsets, permissions
from .serializers import WalletSerializer
from gateway.models import Gateway

class WalletViewSet(viewsets.ModelViewSet):
    """ViewSet for managing Wallets."""
    serializer_class = WalletSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wallet.objects.filter(gateway__user=self.request.user)
    
    def perform_create(self, serializer):
        gateway = Gateway.objects.get(user=self.request.user)
        serializer.save(gateway=gateway)

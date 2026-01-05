from django.shortcuts import render
from .models import Gateway
from .serializers import GatewaySerializer
from rest_framework import viewsets, permissions


class GatewayViewSet(viewsets.ModelViewSet):
    "CRUD API for Gateways"
    serializer_class = GatewaySerializer
    permission_classes = [permissions.IsAuthenticated]


    def get_queryset(self):
        return Gateway.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


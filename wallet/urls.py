from django.urls import path, include
from .views import WalletViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'wallets', WalletViewSet, basename='wallet')
urlpatterns = [
    path('', include(router.urls)),
]

from django.urls import path, include
from .views import PublicPaylinkView, PaylinkCheckoutView, PayLinkViewSet

from rest_framework.routers import DefaultRouter
router = DefaultRouter()
router.register(r'paylinks', PayLinkViewSet, basename='paylink')

urlpatterns = [
    path('paylink/pay/<str:code>/', PublicPaylinkView.as_view(), name='paylink-detail'),
    path('paylink/pay/<str:code>/checkout/', PaylinkCheckoutView.as_view(), name='paylink-create-transaction'),
    path('', include(router.urls)),
    
]
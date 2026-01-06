from django.urls import path, include
from .views import TransactionViewet, MockPaymentConfirmView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'transactions', TransactionViewet, basename='transaction')
urlpatterns = [
    path('', include(router.urls)),
    path('mock-payment/confirm/<str:payment_UID>/', MockPaymentConfirmView.as_view(), name='mock-payment-confirm'),
]
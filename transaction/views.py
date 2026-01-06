from django.shortcuts import get_object_or_404, render
from .models import Transaction
from .serializers import TransactionSerializer, MockPaymentSerializer
from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import transaction as db_transaction
from paylink.models import Paylink

class TransactionViewet(viewsets.ReadOnlyModelViewSet):
    """ViewSet for viewing Transactions."""
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(gateway__user=self.request.user).order_by('-created_at')
    

class MockPaymentConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request, payment_UID):
        transaction_obj = get_object_or_404(Transaction, payment_UID=payment_UID, status='pending')
        print(transaction_obj)

        serializer = MockPaymentSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        if data['paid_amount'] != transaction_obj.amount:
            transaction_obj.status = 'mismatch'
            transaction_obj.save()
            return Response({"detail": "Paid amount is not the required amount."}, status=400)
        
        with db_transaction.atomic():
            try:
                paylink = Paylink.objects.select_for_update().get(id=transaction_obj.paylink_id) 
            except Paylink.DoesNotExist:
                Response({"detail": "Associated paylink not found."}, status=400)

            if paylink.limited_uses is not None:
                successful_transactions_count = Transaction.objects.filter(
                    paylink=paylink,
                    status='success'
                ).count()
                if successful_transactions_count >= paylink.limited_uses:
                    return Response({"detail": "This paylink has reached its usage limit."}, status=400)  


            transaction_obj.status = 'success'
            if data.get('transaction_hash'):
                transaction_obj.transaction_hash = data['transaction_hash']
            transaction_obj.save()
            return Response({"detail": "Payment confirmed successfully."}, status=200)



        
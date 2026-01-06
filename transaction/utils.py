from django.utils.crypto import get_random_string
from .models import Transaction

def generate_unique_payment_uid():
    for _ in range(5):
        uid = get_random_string(12)
        if not Transaction.objects.filter(payment_UID=uid).exists():
            return uid
    raise Exception("Unable to generate unique payment_UID")

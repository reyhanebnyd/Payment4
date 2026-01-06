import uuid

def generate_unique_code():
    """Generate a unique code for Paylink."""
    return uuid.uuid4().hex[:12]




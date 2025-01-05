import re
from django.core.exceptions import ValidationError

def validate_email(email):
    """
    Validate email format using regex pattern
    """
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    if not re.match(pattern, email):
        raise ValidationError('Please enter a valid email address')
    return email


def validate_required(value):
    """
    Validate that a field has a value
    Raises ValidationError if value is empty or None
    """
    if not value:
        raise ValidationError('This field is required')
    return value

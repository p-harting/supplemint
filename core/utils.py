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


def validate_max_length(value, max_length, field_name):
    """
    Validate that a string value doesn't exceed max length
    """
    if len(value) > max_length:
        raise ValidationError(
            f'{field_name} cannot exceed {max_length} characters'
        )
    return value


def validate_numeric(value, field_name):
    """
    Validate that a value is numeric (int or float)
    """
    if not str(value).replace('.', '', 1).isdigit():
        raise ValidationError(
            f'{field_name} must be a number'
        )
    return value


def validate_positive_number(value, field_name):
    """
    Validate that a number is positive
    """
    if float(value) < 0:
        raise ValidationError(
            f'{field_name} must be a positive number'
        )
    return value

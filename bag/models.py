from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

class DiscountCode(models.Model):
    """Model to represent discount codes with a unique code, discount amount, and remaining balance."""
    
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]  # Ensure non-negative values
    )
    remaining_balance = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        validators=[MinValueValidator(0)]  # Ensure non-negative values
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Override save to generate default values for 'code' and 'remaining_balance' if not provided."""
        if not self.code:
            self.code = get_random_string(8).upper()
        if not self.remaining_balance:
            self.remaining_balance = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        """Return a string representation of the discount code and its remaining balance."""
        return f"{self.code} (${self.remaining_balance} remaining)"

    def apply_discount(self, total):
        """Apply the discount to the given total.

        If the remaining balance is greater than or equal to the total, the total is fully discounted.
        Otherwise, apply the remaining balance as a partial discount.
        """
        if self.remaining_balance >= total:
            return total
        else:
            return self.remaining_balance

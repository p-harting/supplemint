from django.db import models
from django.core.validators import MinValueValidator
from django.utils.crypto import get_random_string

class DiscountCode(models.Model):
    code = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    remaining_balance = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.code:
            self.code = get_random_string(8).upper()
        if not self.remaining_balance:
            self.remaining_balance = self.amount
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.code} (${self.remaining_balance} remaining)"

    def apply_discount(self, total):
        if self.remaining_balance >= total:
            return total
        else:
            return self.remaining_balance

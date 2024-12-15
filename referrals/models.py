from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referral_code')
    code = models.CharField(max_length=10, unique=True, default=get_random_string)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.code

class Referral(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referrals')
    referred_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='referred_by')
    commission_earned = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    purchase_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.referrer} referred {self.referred_user}"

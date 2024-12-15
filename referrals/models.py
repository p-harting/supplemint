from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f"{self.user.username}'s referral code: {self.code}"

    @receiver(post_save, sender=User)
    def create_referral_code(sender, instance, created, **kwargs):
        if created:
            ReferralCode.objects.create(
                user=instance,
                code=str(uuid.uuid4())[:8].upper()
            )

class ReferralTransaction(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_earnings')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_purchases')
    order_number = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Referral commission for order {self.order_number}"
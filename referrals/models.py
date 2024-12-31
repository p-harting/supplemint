from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class ReferralCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=12, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    total_earnings = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    unredeemed_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_balances(self):
        total_earnings = ReferralTransaction.objects.filter(
            referrer=self.user,
            commission__gt=0
        ).aggregate(Sum('commission'))['commission__sum'] or 0
        
        redeemed_amount = ReferralTransaction.objects.filter(
            referrer=self.user,
            commission__lt=0
        ).aggregate(Sum('commission'))['commission__sum'] or 0
        
        self.total_earnings = total_earnings
        self.unredeemed_balance = max(0, total_earnings + redeemed_amount)
        self.save()

    def __str__(self):
        return f"{self.user.username}'s referral code: {self.code}"

class ReferralTransaction(models.Model):
    referrer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_earnings')
    referred_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='referral_purchases', null=True, blank=True)
    order_number = models.CharField(max_length=32)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    commission = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        referral_code = ReferralCode.objects.get(user=self.referrer)
        
        if self.commission > 0:
            referral_code.total_earnings += self.commission
        
        redeemed_amount = ReferralTransaction.objects.filter(
            referrer=self.referrer,
            commission__lt=0
        ).aggregate(Sum('commission'))['commission__sum'] or 0
        referral_code.unredeemed_balance = referral_code.total_earnings + redeemed_amount
        
        referral_code.unredeemed_balance = max(0, referral_code.unredeemed_balance)
        referral_code.save()

    def __str__(self):
        return f"Referral commission for order {self.order_number}"

@receiver(post_save, sender=User)
def create_referral_code(sender, instance, created, **kwargs):
    if created:
        ReferralCode.objects.create(
            user=instance,
            code=str(uuid.uuid4())[:8].upper()
        )

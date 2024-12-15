from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib.auth.models import User
from .models import ReferralCode, ReferralTransaction
from profiles.models import UserProfile

@login_required
def referral_dashboard(request):
    try:
        referral_code = ReferralCode.objects.get(user=request.user)
        transactions = ReferralTransaction.objects.filter(referrer=request.user)
        total_earnings = transactions.aggregate(Sum('commission'))['commission__sum'] or 0
        referred_users = UserProfile.objects.filter(referred_by=request.user).count()

        context = {
            'referral_code': referral_code,
            'transactions': transactions,
            'total_earnings': total_earnings,
            'referred_users': referred_users,
        }
        return render(request, 'referrals/dashboard.html', context)
    except ReferralCode.DoesNotExist:
        return render(request, 'referrals/dashboard.html', {'error': 'No referral code found'})
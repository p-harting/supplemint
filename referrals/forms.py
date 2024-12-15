from django import forms
from allauth.account.forms import SignupForm
from .models import ReferralCode
from profiles.models import UserProfile

class CustomSignupForm(SignupForm):
    referral_code = forms.CharField(max_length=12, required=False)

    def save(self, request):
        user = super().save(request)
        referral_code = self.cleaned_data.get('referral_code')
        
        if referral_code:
            try:
                referrer_code = ReferralCode.objects.get(code=referral_code)
                profile = UserProfile.objects.get(user=user)
                profile.referred_by = referrer_code.user
                profile.save()
            except ReferralCode.DoesNotExist:
                pass
                
        return user
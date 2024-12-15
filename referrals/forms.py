from django import forms
from allauth.account.forms import SignupForm

class CustomSignupForm(SignupForm):
    referral_code = forms.CharField(max_length=12, required=False)

    def save(self, request):
        user = super().save(request)
        referral_code = self.cleaned_data.get('referral_code')
        
        if referral_code:
            try:
                referrer_code = ReferralCode.objects.get(code=referral_code)
                user.referred_by = referrer_code.user
                user.save()
            except ReferralCode.DoesNotExist:
                pass
                
        return user
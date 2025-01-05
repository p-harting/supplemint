from django import forms
from allauth.account.forms import SignupForm
from .models import ReferralCode
from profiles.models import UserProfile

class CustomSignupForm(SignupForm):
    """
    Extends the default SignupForm to include an optional referral code field.
    """
    referral_code = forms.CharField(max_length=12, required=False)

    def save(self, request):
        """
        Overrides the save method to handle referral code logic.
        If a valid referral code is provided, associates the new user with the referrer.
        """
        user = super().save(request)  # Save the user using the parent class method
        referral_code = self.cleaned_data.get('referral_code')  # Get the referral code from the form

        if referral_code:
            try:
                # Check if the referral code exists and associate the referrer with the new user
                referrer_code = ReferralCode.objects.get(code=referral_code)
                profile = UserProfile.objects.get(user=user)
                profile.referred_by = referrer_code.user
                profile.save()
            except ReferralCode.DoesNotExist:
                # Silently ignore invalid referral codes
                pass
                
        return user

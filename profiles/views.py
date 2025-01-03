from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import UserProfile
from .forms import UserProfileForm

def profile(request):
    """ Display and handle the user's profile. """
    profile = get_object_or_404(UserProfile, user=request.user)
    
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')
        else:
            messages.error(request, 'Update failed. Please check the form.')
    else:
        profile_form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'
    orders = profile.orders.all().order_by('-date')
    
    context = {
        'profile': profile,
        'profile_form': profile_form,
        'orders': orders,
        'on_profile_page': True
    }

    return render(request, template, context)

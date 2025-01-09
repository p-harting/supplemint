from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import UserProfile
from .forms import UserProfileForm


@login_required
def profile(request):
    """Display and handle the user's profile."""
    # Retrieve the UserProfile for the current logged-in user
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        # Bind the form with POST data and the current profile instance
        profile_form = UserProfileForm(request.POST, instance=profile)

        if profile_form.is_valid():
            # Save the form if it is valid
            profile_form.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('profile')  # Redirect to the same profile page
        else:
            # Show error message if form is invalid
            messages.error(request, 'Update failed. Please check the form.')
    else:
        # Initialize the form with the current profile data
        profile_form = UserProfileForm(instance=profile)

    template = 'profiles/profile.html'

    # Retrieve the user's orders, ordered by date (most recent first)
    orders = profile.orders.all().order_by('-date')
    paginator = Paginator(orders, 5)  # Show 5 orders per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'profile': profile,
        'profile_form': profile_form,
        'orders': page_obj,
        'on_profile_page': True
    }

    # Render the profile template with the context data
    return render(request, template, context)

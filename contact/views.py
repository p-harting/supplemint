from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ContactForm

def contact_view(request):
    """
    Handles the contact form submission.
    
    If POST request, validates and saves the form. Displays success message and redirects.
    If GET request, renders an empty form.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()  # Save the contact message
            messages.success(request, 'Ihre Nachricht wurde erfolgreich gesendet.')
            return redirect('contact')  # Redirect after successful submission
    else:
        form = ContactForm()  # Empty form for GET request

    return render(request, 'contact/contact.html', {'form': form})

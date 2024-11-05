from django.shortcuts import render, redirect, reverse
from django.contrib import messages

from .forms import OrderForm

def checkout(request):
    bag = request.session.get('bag', {})
    if not bag:
        messages.error(request, "There's nothing in your bag at the moment")
        return redirect(reverse('products'))

    order_form = OrderForm()
    template = 'checkout/checkout.html'
    context = {
        'order_form': order_form,
        'stripe_public_key': 'pk_test_51QHj2bJ32Fk3PYAyy99BsOuZClm47x0wRNTDvqPfzkKxzSAngUT7ul3JJGM0Qn4PepkAcI0fu2zY94IvQU268m0P00DidpIweW',
        'client_secret': 'testsecret',
    }

    return render(request, template, context)
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import ReferralCode, ReferralTransaction
from profiles.models import UserProfile
from bag.models import DiscountCode


def calculate_redeemable_balance(total_earnings, redeemed_amount):
    """
    Calculate the redeemable balance by rounding down to the nearest $10.
    """
    available_balance = total_earnings - redeemed_amount
    return max(0, (available_balance // 10) * 10)


@login_required
def referral_dashboard(request):
    """
    Render the referral dashboard, displaying the user's referral statistics
    and transactions.
    """
    try:
        referral_code = ReferralCode.objects.get(user=request.user)
        referral_code.update_balances()

        transactions = ReferralTransaction.objects.filter(
            referrer=request.user)
        total_earnings = referral_code.total_earnings
        redeemed_amount = (
            referral_code.total_earnings -
            referral_code.unredeemed_balance)
        redeemable_balance = calculate_redeemable_balance(
            referral_code.total_earnings, redeemed_amount)
        referred_users = UserProfile.objects.filter(
            referred_by=request.user).count()

        context = {
            'referral_code': referral_code,
            'transactions': transactions,
            'total_earnings': total_earnings,
            'redeemable_balance': redeemable_balance,
            'referred_users': referred_users,
        }
        return render(request, 'referrals/dashboard.html', context)
    except ReferralCode.DoesNotExist:
        return render(
            request,
            'referrals/dashboard.html', {'error': 'No referral code found'})


@csrf_exempt
@login_required
def redeem_balance(request):
    """
    Handle the redemption of referral balances into discount codes.
    """
    if request.method == 'POST':
        try:
            referral_code = ReferralCode.objects.get(user=request.user)
            transactions = ReferralTransaction.objects.filter(
                referrer=request.user)
            redeemed_amount = (
                referral_code.total_earnings -
                referral_code.unredeemed_balance)
            redeemable_balance = calculate_redeemable_balance(
                referral_code.total_earnings, redeemed_amount)

            if redeemable_balance < 10 or redeemable_balance <= 0:
                return JsonResponse({
                    'success': False,
                    'message': 'Minimum redeemable balance is $10'
                })

            discount_code = DiscountCode.objects.create(
                amount=redeemable_balance,
                remaining_balance=redeemable_balance
            )

            referral_code.unredeemed_balance -= redeemable_balance
            referral_code.save()

            ReferralTransaction.objects.create(
                referrer=request.user,
                amount=redeemable_balance,
                commission=-redeemable_balance,
                description=f"Redeemed ${redeemable_balance} as discount "
                f"code {discount_code.code}",
                order_number=f"REDEEM-{discount_code.code}"
            )

            return JsonResponse({
                'success': True,
                'discount_code': discount_code.code,
                'amount': redeemable_balance
            })
        except ReferralCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No referral code found'
            })
        except Exception as e:
            print(f"Unexpected error during redemption: {str(e)}")
            return JsonResponse({
                'success': False,
                'message': 'An unexpected error occurred'
            })
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    })

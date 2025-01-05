/**
 * Copies the referral code to the clipboard.
 */
function copyCode() {
    const code = document.getElementById('referralCode').textContent;
    navigator.clipboard.writeText(code);
    alert('Referral code copied!');
}

/**
 * Copies the referral link to the clipboard.
 */
function copyLink() {
    const link = document.getElementById('referralLink').textContent;
    navigator.clipboard.writeText(link);
    alert('Referral link copied!');
}

// Modal-related logic
const modal = document.getElementById('redeemModal');
const closeModal = document.querySelector('.close-modal');

// Redeem button logic
const redeemButton = document.getElementById('redeemButton');
if (redeemButton) {
    redeemButton.addEventListener('click', function (e) {
        e.preventDefault();
        redeemBalance();
    });
}

// Close modal when the close button is clicked
closeModal.onclick = function () {
    modal.style.display = 'none';
};

// Close modal when clicking outside the modal
window.onclick = function (event) {
    if (event.target == modal) {
        modal.style.display = 'none';
    }
};

/**
 * Copies the discount code from the modal to the clipboard.
 */
function copyDiscountCode() {
    const code = document.getElementById('discountCode').textContent;
    navigator.clipboard.writeText(code);
    alert('Discount code copied!');
}

/**
 * Sends a request to redeem the balance and displays the discount code.
 */
function redeemBalance() {
    fetch(redeemBalanceUrl, {
        method: 'POST',
        headers: {
            'X-CSRFToken': csrfToken,
            'Content-Type': 'application/json',
        },
        credentials: 'same-origin',
    })
        .then((response) => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then((data) => {
            if (data && data.success) {
                const discountCodeElement = document.getElementById('discountCode');
                const discountValueElement = document.getElementById('discountValue');

                discountCodeElement.textContent = data.discount_code;

                const amount = parseFloat(data.amount);
                discountValueElement.textContent = !isNaN(amount)
                    ? `$${amount.toFixed(2)}`
                    : '$0.00';

                const redeemBtn = document.querySelector('.redeem-btn');
                if (redeemBtn) {
                    redeemBtn.textContent = `Redeem $0.00`;
                    redeemBtn.disabled = true;
                    redeemBtn.classList.add('disabled');
                }

                modal.style.display = 'block';
            } else {
                alert('Error: ' + data.message);
            }
        })
        .catch((error) => {
            console.error('Error:', error);
            alert('An error occurred while processing your request');
        });
}

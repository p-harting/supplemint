document.addEventListener('DOMContentLoaded', function() {
    // Discount code application logic
    const applyDiscountBtn = document.getElementById('apply-discount');
    const discountCodeInput = document.getElementById('discount_code');
    const discountMessage = document.getElementById('discount-message');
    const grandTotalElement = document.querySelector('.totals-values p:last-child strong');
    const paymentWarning = document.querySelector('.payment-warning strong');

    applyDiscountBtn.addEventListener('click', function() {
        const code = discountCodeInput.value.trim();
        if (!code) return;

        const form = document.getElementById('payment-form');
        const discountUrl = form.dataset.discountUrl;
        const csrfToken = form.dataset.csrfToken;

        fetch(discountUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrfToken
            },
            body: `discount_code=${encodeURIComponent(code)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update totals and display success message
                discountMessage.textContent = data.message;
                discountMessage.classList.remove('text-danger');
                discountMessage.classList.add('text-success');
                const formattedTotal = parseFloat(data.new_total).toFixed(2);
                grandTotalElement.textContent = `$${formattedTotal}`;
                paymentWarning.textContent = `$${formattedTotal}`;
            } else {
                // Display error message
                discountMessage.textContent = data.message;
                discountMessage.classList.remove('text-success');
                discountMessage.classList.add('text-danger');
            }
        })
        .catch(error => {
            // Handle fetch errors
            discountMessage.textContent = 'An error occurred. Please try again.';
            discountMessage.classList.remove('text-success');
            discountMessage.classList.add('text-danger');
        });
    });
});

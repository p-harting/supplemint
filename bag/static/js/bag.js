document.addEventListener('DOMContentLoaded', function () {
    const quantityInputs = document.querySelectorAll('.quantity-input');
    quantityInputs.forEach(input => {
        const originalValue = input.value;
        const updateButton = input.nextElementSibling;

        // Show the update button when the input value changes
        input.addEventListener('input', function () {
            if (input.value !== originalValue) {
                updateButton.style.display = 'inline-block';
            } else {
                updateButton.style.display = 'none';
            }
        });
    });
});

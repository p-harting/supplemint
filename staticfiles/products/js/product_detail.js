// Dropdown functionality
function toggleDropdown(id) {
    const content = document.getElementById(id);
    const allDropdowns = document.querySelectorAll('.dropdown-product-content');
    const button = content.previousElementSibling;
    const icon = button.querySelector('i');

    allDropdowns.forEach(dropdown => {
        if (dropdown.id !== id && dropdown.style.display === 'block') {
            dropdown.style.display = 'none';
            dropdown.previousElementSibling.querySelector('i').classList.remove('fa-chevron-up');
            dropdown.previousElementSibling.querySelector('i').classList.add('fa-chevron-down');
        }
    });

    if (content.style.display === 'block') {
        content.style.display = 'none';
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    } else {
        content.style.display = 'block';
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    }
}

// Size selector and price update functionality
document.addEventListener('DOMContentLoaded', () => {
    const sizeSelector = document.getElementById('id_product_size');
    const priceDisplay = document.getElementById('product-price');

    const updateDisplayPrice = () => {
        if (sizeSelector && priceDisplay) {
            const selectedOption = sizeSelector.options[sizeSelector.selectedIndex];
            const originalPrice = parseFloat(selectedOption.getAttribute('data-original-price'));
            const salePercentage = parseFloat(selectedOption.getAttribute('data-sale-percentage'));
            
            if (originalPrice) {
                if (salePercentage > 0) {
                    const discountAmount = originalPrice * (salePercentage / 100);
                    const salePrice = (originalPrice - discountAmount).toFixed(2);
                    
                    // Show both prices with strikethrough for original
                    priceDisplay.innerHTML = `
                        <span class="original-price">$${originalPrice.toFixed(2)}</span>
                        <span class="sale-price">$${salePrice}</span>
                    `;
                } else {
                    // Show only original price
                    priceDisplay.innerHTML = `$${originalPrice.toFixed(2)}`;
                }
            }
        }
    };

    if (sizeSelector) {
        updateDisplayPrice();
        sizeSelector.addEventListener('change', updateDisplayPrice);

        // Set initial selected option based on base price
        const basePrice = sizeSelector.getAttribute('data-base-price');
        for (let option of sizeSelector.options) {
            if (option.getAttribute('data-price') == basePrice) {
                option.selected = true;
                break;
            }
        }
    }
});

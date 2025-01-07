class PriceFilter {
    constructor() {
        this.rangeInputs = document.querySelectorAll(".range-input input");
        this.priceInputs = document.querySelectorAll(".price-input input");
        this.range = document.querySelector(".slider .progress");
        this.productCards = document.querySelectorAll('.product-card');
        this.priceGap = 2;
        this.saleFilterBtn = document.getElementById('sale-filter-btn');
        this.showSaleOnly = false;

        this.init();
    }

    getPriceRange() {
        let minPrice = Infinity;
        let maxPrice = -Infinity;

        this.productCards.forEach(card => {
            const salePriceElement = card.querySelector('.sale-price');
            const priceElement = salePriceElement || card.querySelector('.product-price');
            
            if (priceElement) {
                const price = parseFloat(priceElement.textContent.replace('$', ''));
                minPrice = Math.min(minPrice, price);
                maxPrice = Math.max(maxPrice, price);
            }
        });

        // If no prices found, use default range
        if (minPrice === Infinity || maxPrice === -Infinity) {
            return { min: 1, max: 100 };
        }

        // Round to nearest 10
        minPrice = Math.floor(minPrice / 10) * 10;
        maxPrice = Math.ceil(maxPrice / 10) * 10;

        return { min: minPrice, max: maxPrice };
    }

    init() {
        // Set range input accent color
        this.rangeInputs.forEach(input => {
            input.style.accentColor = '#ADEBB3';
        });

        // Get actual price range from products
        const { min, max } = this.getPriceRange();
        
        // Update range inputs
        this.rangeInputs[0].min = min;
        this.rangeInputs[0].max = max;
        this.rangeInputs[0].value = min;
        
        this.rangeInputs[1].min = min;
        this.rangeInputs[1].max = max;
        this.rangeInputs[1].value = max;

        // Update price inputs
        this.priceInputs[0].value = min;
        this.priceInputs[1].value = max;

        // Initialize event listeners
        this.setupRangeInputListeners();
        this.setupSaleFilterListener();

        // Initial filter
        this.filterProductsByPrice(min, max);
    }

    filterProductsByPrice(minPrice, maxPrice) {
        this.productCards.forEach(card => {
            // Check for sale price first, then regular price
            const salePriceElement = card.querySelector('.sale-price');
            const priceElement = salePriceElement || card.querySelector('.product-price');
            
            if (!priceElement) {
                card.style.display = 'none';
                return;
            }

            const price = parseFloat(priceElement.textContent.replace('$', ''));
            const isSale = card.querySelector('.sale-badge') !== null;
            const isInPriceRange = price >= minPrice && price <= maxPrice;

            if (this.showSaleOnly) {
                card.style.display = isSale && isInPriceRange ? 'block' : 'none';
            } else {
                card.style.display = isInPriceRange ? 'block' : 'none';
            }
        });
    }

    validatePrice(value) {
        const num = parseInt(value);
        if (isNaN(num)) return false;
        return num >= 0 && num <= 100;
    }

    setupRangeInputListeners() {
        this.rangeInputs.forEach((input, index) => {
            input.addEventListener("input", (e) => {
                // Validate price inputs
                const minVal = parseInt(this.rangeInputs[0].value);
                const maxVal = parseInt(this.rangeInputs[1].value);
                
                if (!this.validatePrice(minVal) || !this.validatePrice(maxVal)) {
                    return;
                }

                if (maxVal - minVal < this.priceGap) {
                    if (e.target.className === "range-min") {
                        this.rangeInputs[0].value = maxVal - this.priceGap;
                    } else {
                        this.rangeInputs[1].value = minVal + this.priceGap;
                    }
                } else {
                    this.priceInputs[0].value = minVal;
                    this.priceInputs[1].value = maxVal;
                    this.range.style.left = (minVal / this.rangeInputs[0].max) * 100 + "%";
                    this.range.style.right = 100 - (maxVal / this.rangeInputs[1].max) * 100 + "%";
                    this.filterProductsByPrice(minVal, maxVal);
                }
            });
        });
    }

    setupPriceInputListeners() {
        this.priceInputs.forEach((input, index) => {
            input.addEventListener('input', (e) => {
                let value = parseInt(input.value);
                if (isNaN(value)) {
                    value = 0;
                }
                value = Math.min(Math.max(value, 0), 100);
                input.value = value;
                
                // Update corresponding range input
                const rangeInput = this.rangeInputs[index];
                rangeInput.value = input.value;

                // Trigger range input event to update filter
                rangeInput.dispatchEvent(new Event('input'));
            });
        });
    }

    setupSaleFilterListener() {
        this.saleFilterBtn.addEventListener('click', () => {
            this.showSaleOnly = !this.showSaleOnly;
            this.saleFilterBtn.classList.toggle('active', this.showSaleOnly);

            const minPrice = parseInt(this.priceInputs[0].value);
            const maxPrice = parseInt(this.priceInputs[1].value);
            this.filterProductsByPrice(minPrice, maxPrice);
        });
    }
}

// Initialize price filter when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new PriceFilter();
});

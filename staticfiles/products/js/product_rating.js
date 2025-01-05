document.addEventListener('DOMContentLoaded', function() {
    function initializeRatings() {
        document.querySelectorAll('.product-rating').forEach(function(ratingElement) {
            const rating = parseFloat(ratingElement.getAttribute('data-rating'));
            if (!rating) return;

            const fullStars = Math.floor(rating);
            const halfStar = (rating - fullStars) >= 0.5;
            const emptyStars = 5 - fullStars - (halfStar ? 1 : 0);

            let starsHTML = '';

            // Add full stars
            starsHTML += '<i class="fas fa-star" style="color: gold;"></i>'.repeat(fullStars);

            // Add half star if needed
            if (halfStar) {
                starsHTML += '<i class="fas fa-star-half-alt" style="color: gold;"></i>';
            }

            // Add empty stars
            starsHTML += '<i class="far fa-star" style="color: gray;"></i>'.repeat(emptyStars);

            ratingElement.innerHTML = starsHTML;
        });
    }

    initializeRatings();
});
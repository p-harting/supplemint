function loadPage(page) {
    const reviewsContainer = document.querySelector('.reviews-container');
    const productId = document.querySelector('[data-product-id]').dataset.productId;
    const sortValue = document.getElementById('review-sort').value;

    fetch(`/reviews/sort/${productId}/?sort=${sortValue}&page=${page}`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.html) {
            reviewsContainer.innerHTML = data.html;
        }
    })
    .catch(error => console.error('Error:', error));
}

function sortReviews(sortValue) {
    const reviewsContainer = document.querySelector('.reviews-container');
    const productId = document.querySelector('[data-product-id]').dataset.productId;

    fetch(`/reviews/sort/${productId}/?sort=${sortValue}&page=1`, {
        headers: {
            'X-Requested-With': 'XMLHttpRequest'
        }
    })
    .then(response => response.json())
    .then(data => {
        if (data.html) {
            reviewsContainer.innerHTML = data.html;
        }
    })
    .catch(error => console.error('Error:', error));
}
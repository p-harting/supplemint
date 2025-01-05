// Add Review functionality
function addReview(productId) {
    fetch(`/reviews/add/${productId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.form_html) {
                document.getElementById('modalContent').innerHTML = data.form_html;
                reviewModal.openModal();
                setupFormSubmitHandler(productId);
            }
        });
}

function setupFormSubmitHandler(productId) {
    const form = document.getElementById('reviewForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(`/reviews/add/${productId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                reviewModal.closeModal();
                location.reload();
            }
        });
    });
}

// Edit Review functionality
function editReview(reviewId) {
    fetch(`/reviews/edit/${reviewId}/`)
        .then(response => response.json())
        .then(data => {
            if (data.form_html) {
                document.getElementById('modalContent').innerHTML = data.form_html;
                reviewModal.openModal();
                setupEditFormSubmitHandler(reviewId);
            }
        })
        .catch(error => console.error('Error:', error));
}

function setupEditFormSubmitHandler(reviewId) {
    const form = document.getElementById('reviewForm');
    form.addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);

        fetch(`/reviews/edit/${reviewId}/`, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                reviewModal.closeModal();
                location.reload();
            }
        })
        .catch(error => console.error('Error:', error));
    });
}

// Delete Review functionality
function deleteReview(reviewId) {
    if (confirm('Are you sure you want to delete this review?')) {
        fetch(`/reviews/delete/${reviewId}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                location.reload();
            }
        });
    }
}
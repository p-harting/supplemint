document.getElementById('reviewForm').addEventListener('submit', function(e) {
    e.preventDefault();  // Prevent default form submission
    
    const formData = new FormData(this);
    const reviewId = this.dataset.reviewId;
    const productId = this.dataset.productId;
    
    // Determine the correct URL based on whether we're editing or adding a review
    const url = reviewId ? `/reviews/edit/${reviewId}/` : `/reviews/add/${productId}/`;
    
    // Send the form data using fetch
    fetch(url, {
        method: 'POST',
        body: formData,
        headers: {
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value  // Use the CSRF token from the form
        }
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            closeModal();  // Close modal if successful
            location.reload();  // Reload page to show updated review
        } else if (data.errors) {
            console.error('Form errors:', data.errors);  // Log form errors
        }
    })
    .catch(error => {
        console.error('Error:', error);  // Log any other errors
    });
});

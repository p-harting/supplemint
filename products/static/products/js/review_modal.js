class ReviewModal {
    constructor() {
        this.modal = document.getElementById("reviewModal");
        this.span = document.getElementsByClassName("close")[0];
        this.setupEventListeners();
    }

    setupEventListeners() {
        this.span.onclick = () => this.closeModal();
        window.onclick = (event) => {
            if (event.target == this.modal) {
                this.closeModal();
            }
        };
    }

    openModal() {
        this.modal.style.display = "block";
    }

    closeModal() {
        this.modal.style.display = "none";
    }
}

// CSRF token helper
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Initialize modal
const reviewModal = new ReviewModal();
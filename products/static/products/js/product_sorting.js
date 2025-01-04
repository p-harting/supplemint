document.addEventListener('DOMContentLoaded', function() {
    const sortSelector = document.getElementById('sort-selector');
    
    sortSelector.addEventListener('change', function() {
        const currentUrl = new URL(window.location);
        const selectedVal = this.value;

        if (selectedVal !== "reset") {
            const [sort, direction] = selectedVal.split("_");
            currentUrl.searchParams.set("sort", sort);
            currentUrl.searchParams.set("direction", direction);
        } else {
            currentUrl.searchParams.delete("sort");
            currentUrl.searchParams.delete("direction");
        }

        window.location.replace(currentUrl);
    });

    // Back to top functionality
    const bttLink = document.querySelector('.btt-link');
    if (bttLink) {
        bttLink.addEventListener('click', function(e) {
            window.scrollTo(0, 0);
        });
    }
});
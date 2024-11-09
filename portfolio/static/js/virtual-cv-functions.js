document.addEventListener("DOMContentLoaded", function () {
    const floatingButton = document.getElementById("floating-buttons");
    const header = document.getElementById("download-button");

    // Function to check if the header is visible
    function isHeaderVisible() {
        const headerRect = header.getBoundingClientRect();
        return headerRect.bottom > 0; // Check if header is still in the viewport
    }

    // Scroll event to toggle fixed position
    window.addEventListener("scroll", function () {
        if (!isHeaderVisible()) {
            floatingButton.style.display = "block";
        } else {
            floatingButton.style.display = "none";
        }
    });
});

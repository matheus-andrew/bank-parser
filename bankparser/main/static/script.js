document.addEventListener("DOMContentLoaded", function () {
    const container = document.querySelector(".container");
    const tableContainer = document.querySelector(".table-container");

    // Function to trigger container resizing
    function expandContainer() {
        if (tableContainer && tableContainer.scrollHeight > 0) {
            // Dynamically set the height of the container to fit the content
            const newHeight = container.scrollHeight + tableContainer.scrollHeight + 20; // Adjust height dynamically
            container.style.maxHeight = `${newHeight}px`;
        }
    }

    // Observe changes in the DOM to detect when the table appears
    const observer = new MutationObserver((mutations) => {
        mutations.forEach((mutation) => {
            if (mutation.addedNodes.length > 0) {
                expandContainer();
            }
        });
    });

    // Start observing the table's parent container for changes
    observer.observe(tableContainer, { childList: true });
});
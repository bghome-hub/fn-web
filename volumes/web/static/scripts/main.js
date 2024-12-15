// static/scripts/main.js

document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('generate-form');
    const spinner = document.getElementById('loading-spinner');
    const submitBtn = document.getElementById('submit-btn');
    const processingMessage = document.getElementById('processing-message');
    const navbarMenu = document.getElementById('navbar-menu');
    const overlay = document.getElementById('overlay');

    if (form) {
        form.addEventListener('submit', function() {
            // Disable submit button
            submitBtn.disabled = true;
            // Show spinner and message
            spinner.style.display = 'block';
            processingMessage.style.display = 'block';
        });
    }

    

    // Close menu when clicking outside
    overlay.addEventListener('click', function() {
        navbarMenu.classList.remove('active');
        overlay.classList.remove('active');
    });
});
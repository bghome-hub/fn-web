// static/scripts/main.js

document.addEventListener('DOMContentLoaded', function() {
    const articleForm = document.getElementById('generate-article-form');
    const storyForm = document.getElementById('generate-story-form');
    const spinner = document.getElementById('loading-spinner');
    const processingMessage = document.getElementById('processing-message');
    const navbarMenu = document.getElementById('navbar-menu');
    const overlay = document.getElementById('overlay');
    const backupForm = document.querySelector('form[action="{{ url_for(\'db_backup\') }}"]');
    const restoreForm = document.querySelector('form[action="{{ url_for(\'db_restore\') }}"]');

    if (articleForm) {
        articleForm.addEventListener('submit', function() {
            // Disable submit button
            document.getElementById('submit-article-btn').disabled = true;
            // Show spinner and message
            spinner.style.display = 'block';
            processingMessage.style.display = 'block';
        });
    }

    if (storyForm) {
        storyForm.addEventListener('submit', function() {
            // Disable submit button
            document.getElementById('submit-story-btn').disabled = true;
            // Show spinner and message
            spinner.style.display = 'block';
            processingMessage.style.display = 'block';
        });
    }

    if (backupForm) {
        backupForm.addEventListener('submit', function(event) {
            const dbBackupSelect = document.getElementById('db_backup');
            if (!dbBackupSelect.value) {
                alert('Please select a database to backup.');
                event.preventDefault();
            }
        });
    }

    if (restoreForm) {
        restoreForm.addEventListener('submit', function(event) {
            const dbRestoreSelect = document.getElementById('db_restore');
            const backupFileInput = document.getElementById('backup_file');
            if (!dbRestoreSelect.value) {
                alert('Please select a database to restore.');
                event.preventDefault();
            }
            if (!backupFileInput.value) {
                alert('Please select a backup file to restore.');
                event.preventDefault();
            }
        });
    }

    document.querySelectorAll('.delete-article, .delete-story').forEach(button => {
        button.addEventListener('click', function() {
            const resourceType = this.classList.contains('delete-article') ? 'article' : 'story';
            const resourceId = this.getAttribute(`data-${resourceType}-id`);
            
            if (confirm(`Are you sure you want to delete this ${resourceType}?`)) {
                fetch(`/delete_${resourceType}/${resourceId}`, {  // Corrected URL
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        // Remove the resource card from the DOM
                        this.closest(`.${resourceType}-card`).remove();
                        alert(`${resourceType.charAt(0).toUpperCase() + resourceType.slice(1)} deleted successfully.`);
                    } else {
                        alert(`Failed to delete the ${resourceType}: ${data.error}`);
                    }
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert(`An error occurred while deleting the ${resourceType}.`);
                });
            }
        });
    });

    // Close menu when clicking outside
    overlay.addEventListener('click', function() {
        navbarMenu.classList.remove('active');
        overlay.classList.remove('active');
    });

    // Open the default tab
    const defaultTab = document.querySelector('.tablinks');
    if (defaultTab) {
        defaultTab.click();
    }
});

function openTab(evt, tabName) {
    // Hide all tabcontent elements
    const tabcontents = document.getElementsByClassName("tabcontent");
    for (let i = 0; i < tabcontents.length; i++) {
        tabcontents[i].style.display = "none";
    }

    // Remove 'active' class from all tablinks
    const tablinks = document.getElementsByClassName("tablinks");
    for (let i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an 'active' class to the button that opened the tab
    document.getElementById(tabName).style.display = "block";
    evt.currentTarget.className += " active";

    // Update the Recent Section Title and Content
    const recentSectionTitle = document.getElementById('recent-section-title');
    const recentArticles = document.getElementById('recent-articles');
    const recentStories = document.getElementById('recent-stories');

    if (tabName === 'Articles') {
        recentSectionTitle.textContent = 'Recent Articles';
        recentArticles.style.display = 'grid';
        recentStories.style.display = 'none';
    } else if (tabName === 'Stories') {
        recentSectionTitle.textContent = 'Recent Stories';
        recentArticles.style.display = 'none';
        recentStories.style.display = 'grid';
    }
}
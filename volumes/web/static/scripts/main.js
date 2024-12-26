// static/scripts/main.js

document.addEventListener('DOMContentLoaded', function() {
    const articleForm = document.getElementById('generate-article-form');
    const storyForm = document.getElementById('generate-story-form');
    const spinner = document.getElementById('loading-spinner');
    const processingMessage = document.getElementById('processing-message');
    const navbarMenu = document.getElementById('navbar-menu');
    const overlay = document.getElementById('overlay');

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

    document.querySelectorAll('.delete-article').forEach(button => {
        button.addEventListener('click', function() {
            const articleId = this.getAttribute('data-article-id');
            if (confirm('Are you sure you want to delete this article?')) {
                fetch(`/delete_article/${articleId}`, {
                    method: 'DELETE',
                    headers: {
                        'Content-Type': 'application/json'
                    }
                })
                .then(response => {
                    if (response.ok) {
                        location.reload();
                    } else {
                        alert('Failed to delete the article.');
                    }
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
}
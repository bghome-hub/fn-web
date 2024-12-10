const form = document.getElementById('generate-form');
const articlesContainer = document.getElementById('articles');

// Display Message Function
function displayMessage(message, type = 'info') {
    const existingMessage = document.querySelector('.message');
    if (existingMessage) {
        existingMessage.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    document.body.prepend(messageDiv);
    setTimeout(() => messageDiv.remove(), 3000);
}

// Show Loading Indicator
function showLoading() {
    articlesContainer.innerHTML = '<h2>Generated Articles</h2><p>Loading articles...</p>';
}

// Fetch Existing Articles on Load
async function fetchArticles() {
    showLoading();
    try {
        const response = await fetch('/articles');
        if (!response.ok) {
            throw new Error(`Error fetching articles: ${response.statusText}`);
        }
        const articles = await response.json();

        articlesContainer.innerHTML = '<h2>Generated Articles</h2>';

        if (articles.length === 0) {
            articlesContainer.innerHTML += '<p>No articles generated yet.</p>';
            return;
        }

        const ul = document.createElement('ul');

        articles.forEach(article => {
            const li = document.createElement('li');

            li.innerHTML = `
                <h3><a href="/article/${article.id}">${article.title}</a></h3>
                <p><strong>Abstract:</strong> ${article.abstract}</p>
            `;

            ul.appendChild(li);
        });

        articlesContainer.appendChild(ul);
    } catch (error) {
        console.error('Error fetching articles:', error);
        displayMessage('Failed to load articles.', 'error');
        articlesContainer.innerHTML = '<h2>Generated Articles</h2><p>Error loading articles.</p>';
    }
}

// Generate a New Article
form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const topicInput = document.getElementById('topic');
    const topic = topicInput.value.trim();

    if (!topic) {
        displayMessage('Please enter a topic!', 'error');
        return;
    }

    // Disable form and show loading
    form.querySelector('button').disabled = true;
    displayMessage('Generating article...', 'info');

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });

        if (response.ok) {
            const data = await response.json();
            displayMessage('Article generated successfully!', 'success');
            // Redirect to the article detail page
            window.location.href = `/article/${data.article_id}`;
        } else {
            const error = await response.json();
            displayMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        console.error('Error generating article:', error);
        displayMessage('An error occurred while generating the article.', 'error');
    } finally {
        form.querySelector('button').disabled = false;
        topicInput.value = '';
    }
});

// Load Articles on Page Load
document.addEventListener('DOMContentLoaded', fetchArticles);

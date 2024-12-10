const form = document.getElementById('generate-form');
const articlesContainer = document.getElementById('articles');
const spinner = document.getElementById('spinner');
const generateButton = document.getElementById('generate-button');

console.log('Form Element:', form);
console.log('Articles Container:', articlesContainer);
console.log('Spinner Element:', spinner);
console.log('Generate Button:', generateButton);

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

    console.log('Form Submitted. Topic:', topic);

    if (!topic) {
        displayMessage('Please enter a topic!', 'error');
        return;
    }

    // Show spinner and disable button
    spinner.classList.remove('hidden');
    generateButton.disabled = true;
    console.log('Spinner shown and button disabled.');

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ topic }),
        });

        console.log('Response Status:', response.status);

        if (response.ok) {
            const data = await response.json();
            console.log('Article Generated:', data);
            displayMessage('Article generated successfully!', 'success');
            // Redirect to the article detail page
            window.location.href = `/article/${data.article_id}`;
        } else {
            const error = await response.json();
            console.log('Error Response:', error);
            displayMessage(`Error: ${error.error}`, 'error');
        }
    } catch (error) {
        console.error('Error generating article:', error);
        displayMessage('An error occurred while generating the article.', 'error');
    } finally {
        // Hide spinner and enable button
        spinner.classList.add('hidden');
        generateButton.disabled = false;
        topicInput.value = '';
        console.log('Spinner hidden and button enabled.');
    }
});





// Load Articles on Page Load
document.addEventListener('DOMContentLoaded', fetchArticles);

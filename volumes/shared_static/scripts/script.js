let publicBaseUrl = '';  // Initialize a variable to store the public base URL
let ollamaModel = '';    // Initialize a variable to store the Ollama model name

// Fetch the configuration from the Flask backend
document.addEventListener('DOMContentLoaded', async () => {
    try {
        // Fetch configuration data from the backend
        const configResponse = await fetch('/config');
        if (!configResponse.ok) {
            throw new Error('Failed to fetch configuration from backend');
        }

        const config = await configResponse.json();
        publicBaseUrl = config.publicBaseUrl;  // Set the public base URL for later use
        ollamaModel = config.ollamaModel;      // Set the Ollama model name for later use

    } catch (error) {
        console.error('Error fetching configuration:', error);
    }

    // Load recent articles after fetching the configuration
    loadRecentArticles();
});

// Event listener for the form submission
document.getElementById('article-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const topicInput = document.getElementById('topic');
    const topic = topicInput.value.trim();

    if (!topic) {
        alert('Please enter a statement to affirm.');
        return;
    }

    // Disable the form elements while processing
    topicInput.disabled = true;
    e.target.querySelector('button').disabled = true;

    // Show a loading spinner
    const messageDiv = document.getElementById('message');
    const spinner = document.createElement('div');
    spinner.classList.add('spinner');
    messageDiv.innerHTML = ''; // Clear any existing message
    messageDiv.textContent = `Generating article... Please wait, this may take a minute. Connecting to local AI model ${ollamaModel}`;
    messageDiv.appendChild(spinner);

    try {
        // Send request to generate an article
        const response = await fetch('/generate', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ topic })
        });

        const data = await response.json();

        if (response.ok && data.url) {
            // Use the publicBaseUrl fetched from the backend to construct the full article URL
            const fullUrl = `${publicBaseUrl}${data.url}`;

            messageDiv.innerHTML = `
                <p>Article created successfully!</p>
                <p>View it here: <a href="${fullUrl}" target="_blank">${fullUrl}</a></p>
            `;

            // Refresh recent articles
            loadRecentArticles();
        } else {
            messageDiv.innerHTML = `
                <p class="error">Error: ${data.error || 'An unknown error occurred.'}</p>
            `;
        }
    } catch (error) {
        console.error('Error:', error);
        messageDiv.innerHTML = `
            <p class="error">An error occurred while generating the article. Please try again later.</p>
        `;
    } finally {
        // Remove the spinner
        if (spinner) {
            spinner.remove();
        }

        // Re-enable the form elements
        topicInput.disabled = false;
        e.target.querySelector('button').disabled = false;
    }
});

// Function to load recent articles
async function loadRecentArticles() {
    const recentArticlesList = document.getElementById('recent-articles');
    recentArticlesList.innerHTML = "<li>Loading...</li>";
    try {
        const response = await fetch('/articles', {
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        const recentArticlesList = document.getElementById('recent-articles');

        // Clear any existing content
        recentArticlesList.innerHTML = '';

        // Populate the list with articles
        data.forEach(article => {
            const listItem = document.createElement('li');
            listItem.classList.add('article-item');
            listItem.innerHTML = `<a href="${publicBaseUrl}/article/${article.id}">${article.topic}</a>`;
            recentArticlesList.appendChild(listItem);
        });
    } catch (error) {
        console.error("Error while loading recent articles:", error);
    }
}

// static/scripts/all_articles.js

// Rename Modal Elements
const renameModal = document.getElementById('renameModal');
const renameInput = document.getElementById('renameInput');
const confirmRename = document.getElementById('confirmRename');
const closeModal = document.querySelector('.close-modal');
let entryIdToRename = null;

// Open Modal for Rename
document.querySelectorAll('.rename-btn').forEach(button => {
    button.addEventListener('click', (event) => {
        entryIdToRename = event.target.dataset.id;
        renameInput.value = event.target.dataset.title;
        renameModal.style.display = 'block';
    });
});

// Close Modal
closeModal.addEventListener('click', () => {
    renameModal.style.display = 'none';
});

// Confirm Rename
confirmRename.addEventListener('click', async () => {
    const newName = renameInput.value.trim();
    if (newName) {
        try {
            const response = await fetch(`/articles/rename/${entryIdToRename}`, {
                method: 'PUT',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ new_name: newName })
            });
            if (response.ok) {
                // Update the entry title in the DOM
                document.querySelector(`#entry-${entryIdToRename} .entry-title`).textContent = newName;
                renameModal.style.display = 'none';
                alert('Article renamed successfully!');
            } else {
                const errorData = await response.json();
                alert(`Error: ${errorData.error}`);
            }
        } catch (error) {
            console.error('Error:', error);
            alert('An error occurred while renaming the article.');
        }
    } else {
        alert('Please enter a valid title.');
    }
});

// Delete Entry
document.querySelectorAll('.delete-btn').forEach(button => {
    button.addEventListener('click', async (event) => {
        const entryId = event.target.dataset.id;
        const confirmDelete = confirm('Are you sure you want to delete this article?');
        if (confirmDelete) {
            try {
                const response = await fetch(`/articles/delete/${entryId}`, {
                    method: 'DELETE'
                });
                if (response.ok) {
                    // Remove the entry from the DOM
                    document.getElementById(`entry-${entryId}`).remove();
                    alert('Article deleted successfully!');
                } else {
                    const errorData = await response.json();
                    alert(`Error: ${errorData.error}`);
                }
            } catch (error) {
                console.error('Error:', error);
                alert('An error occurred while deleting the article.');
            }
        }
    });
});

// Close modal when clicking outside of it
window.addEventListener('click', (event) => {
    if (event.target == renameModal) {
        renameModal.style.display = 'none';
    }
});

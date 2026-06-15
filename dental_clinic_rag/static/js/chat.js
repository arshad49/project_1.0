// Chat functionality
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const uploadForm = document.getElementById('uploadForm');
    const uploadStatus = document.getElementById('uploadStatus');
    const clearChatBtn = document.getElementById('clearChatBtn');

    // Handle chat form submission
    chatForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;

        // Add user message to chat
        appendMessage('user', message);
        messageInput.value = '';

        // Show loading indicator
        const loadingMsg = appendMessage('bot', '<div class="loading"></div> Thinking...', true);

        try {
            const response = await fetch('/chat/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ message: message })
            });

            const data = await response.json();

            // Remove loading message
            loadingMsg.remove();

            if (response.ok) {
                // Add bot response
                appendMessage('bot', data.response, false, data.sources);
            } else {
                appendMessage('bot', `Error: ${data.error}`);
            }
        } catch (error) {
            loadingMsg.remove();
            appendMessage('bot', `Error: ${error.message}`);
        }

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;
    });

    // Handle PDF upload
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        uploadStatus.className = 'status-message';
        uploadStatus.textContent = 'Uploading and processing PDF...';
        uploadStatus.style.display = 'block';

        try {
            const response = await fetch('/upload-pdf/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                uploadStatus.className = 'status-message success';
                uploadStatus.textContent = data.message;
                uploadForm.reset();
                
                // Reload page to show new document
                setTimeout(() => location.reload(), 1500);
            } else {
                uploadStatus.className = 'status-message error';
                uploadStatus.textContent = data.error;
            }
        } catch (error) {
            uploadStatus.className = 'status-message error';
            uploadStatus.textContent = `Error: ${error.message}`;
        }
    });

    // Handle clear chat
    clearChatBtn.addEventListener('click', async function() {
        if (!confirm('Are you sure you want to clear the chat history?')) return;

        try {
            const response = await fetch('/clear-chat/', {
                method: 'POST',
                headers: {
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });

            const data = await response.json();

            if (response.ok) {
                // Clear chat messages
                chatMessages.innerHTML = `
                    <div class="welcome-message">
                        <i class="fas fa-tooth"></i>
                        <h2>Welcome to Dental Clinic AI Assistant!</h2>
                        <p>I'm here to help you with information about dental care, procedures, appointments, and more. Upload PDF documents to enhance my knowledge base, then ask me anything!</p>
                    </div>
                `;
            } else {
                alert(data.error);
            }
        } catch (error) {
            alert(`Error: ${error.message}`);
        }
    });

    // Helper function to append messages
    function appendMessage(role, content, isHtml = false, sources = null) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${role}-message`;

        const icon = role === 'user' ? 'fa-user' : 'fa-robot';
        const roleText = role.charAt(0).toUpperCase() + role.slice(1);

        let sourcesHtml = '';
        if (sources && sources.length > 0) {
            const sourcesText = sources.map(s => `${s.document} (${(s.similarity * 100).toFixed(0)}% match)`).join(', ');
            sourcesHtml = `
                <div class="message-sources">
                    <small><i class="fas fa-bookmark"></i> Sources: ${sourcesText}</small>
                </div>
            `;
        }

        messageDiv.innerHTML = `
            <div class="message-header">
                <i class="fas ${icon}"></i>
                <span class="message-role">${roleText}</span>
            </div>
            <div class="message-content">
                ${isHtml ? content : content.replace(/\n/g, '<br>')}
            </div>
            ${sourcesHtml}
        `;

        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        return messageDiv;
    }

    // Helper function to get CSRF token
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});

// Global functions for document actions
async function processDocument(documentId) {
    if (!confirm('Re-process this document? This will delete existing chunks and create new ones.')) return;

    try {
        const response = await fetch(`/documents/${documentId}/process/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

async function deleteDocument(documentId) {
    if (!confirm('Are you sure you want to delete this document? This action cannot be undone.')) return;

    try {
        const response = await fetch(`/documents/${documentId}/delete/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            }
        });

        const data = await response.json();

        if (response.ok) {
            alert(data.message);
            location.reload();
        } else {
            alert(data.error);
        }
    } catch (error) {
        alert(`Error: ${error.message}`);
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

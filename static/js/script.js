document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chatForm');
    const messageInput = document.getElementById('messageInput');
    const chatMessages = document.getElementById('chatMessages');
    const imageUploadForm = document.getElementById('imageUploadForm');
    const imageUpload = document.getElementById('imageUpload');
    const imagePreview = document.getElementById('imagePreview');
    const previewImg = document.getElementById('previewImg');
    const analysisResults = document.getElementById('analysisResults');
    const imageQuestion = document.getElementById('imageQuestion');
    const askImageBtn = document.getElementById('askImageBtn');
    const resetBtn = document.getElementById('resetBtn');
    
    let currentImagePath = null;
    
    // Function to add a message to the chat
    function addMessage(content, type) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', type);
        messageDiv.textContent = content;
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to show loading indicator
    function showLoading() {
        const loadingDiv = document.createElement('div');
        loadingDiv.classList.add('message', 'system', 'loading');
        loadingDiv.id = 'loadingIndicator';
        loadingDiv.textContent = 'Thinking...';
        chatMessages.appendChild(loadingDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Function to hide loading indicator
    function hideLoading() {
        const loadingIndicator = document.getElementById('loadingIndicator');
        if (loadingIndicator) {
            loadingIndicator.remove();
        }
    }
    
    // Handle chat form submission
    chatForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const message = messageInput.value.trim();
        if (!message) return;
        
        // Add user message to chat
        addMessage(message, 'user');
        
        // Clear input
        messageInput.value = '';
        
        // Show loading
        showLoading();
        
        // Send message to backend
        fetch('/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ message: message }),
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            hideLoading();
            
            if (data.success) {
                // Add assistant response to chat
                addMessage(data.response, 'assistant');
            } else {
                // Show error
                addMessage('Error: ' + data.error, 'system');
            }
        })
        .catch(error => {
            // Hide loading
            hideLoading();
            
            // Show error
            addMessage('Error: ' + error.message, 'system');
        });
    });
    
    // Handle image upload form submission
    imageUploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        if (!imageUpload.files || imageUpload.files.length === 0) {
            alert('Please select an image to upload');
            return;
        }
        
        // Create form data
        const formData = new FormData();
        formData.append('image', imageUpload.files[0]);
        
        // Show loading message in chat
        addMessage('Uploading and analyzing image...', 'system');
        
        // Upload and analyze image
        fetch('/analyze-image', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Show image preview
                imagePreview.classList.remove('d-none');
                previewImg.src = '/static/' + data.image_path;
                currentImagePath = data.image_path;
                
                // Display analysis results
                let resultsHTML = `<h5 class="mt-3">Analysis Results</h5>
                                  <p>${data.summary}</p>
                                  <h6>Detected objects:</h6>
                                  <ul class="list-group">`;
                
                data.descriptions.forEach(item => {
                    resultsHTML += `
                        <li class="list-group-item">
                            ${item.label} (${item.confidence.toFixed(1)}%)
                            <div class="confidence-bar" style="width: ${item.confidence}%"></div>
                        </li>`;
                });
                
                resultsHTML += `</ul>`;
                analysisResults.innerHTML = resultsHTML;
                
                // Add message to chat
                addMessage(`I've analyzed your image. It appears to be ${data.descriptions[0].label} with ${data.descriptions[0].confidence.toFixed(1)}% confidence.`, 'assistant');
            } else {
                // Show error
                addMessage('Error analyzing image: ' + data.error, 'system');
            }
        })
        .catch(error => {
            // Show error
            addMessage('Error: ' + error.message, 'system');
        });
    });
    
    // Handle image question button click
    askImageBtn.addEventListener('click', function() {
        const question = imageQuestion.value.trim();
        if (!question) {
            alert('Please enter a question about the image');
            return;
        }
        
        if (!currentImagePath) {
            alert('Please upload and analyze an image first');
            return;
        }
        
        // Add question to chat
        addMessage('About the image: ' + question, 'user');
        
        // Show loading
        showLoading();
        
        // Send question to backend
        fetch('/image-question', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
                image_path: currentImagePath,
                question: question 
            }),
        })
        .then(response => response.json())
        .then(data => {
            // Hide loading
            hideLoading();
            
            if (data.success) {
                // Add assistant response to chat
                addMessage(data.response, 'assistant');
            } else {
                // Show error
                addMessage('Error: ' + data.error, 'system');
            }
        })
        .catch(error => {
            // Hide loading
            hideLoading();
            
            // Show error
            addMessage('Error: ' + error.message, 'system');
        });
        
        // Clear input
        imageQuestion.value = '';
    });
    
    // Handle reset button click
    resetBtn.addEventListener('click', function() {
        // Send reset request to backend
        fetch('/reset', {
            method: 'POST',
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Clear chat messages except the first one
                while (chatMessages.childNodes.length > 1) {
                    chatMessages.removeChild(chatMessages.lastChild);
                }
                
                // Add reset message
                addMessage('Conversation has been reset.', 'system');
                
                // Clear image preview
                imagePreview.classList.add('d-none');
                previewImg.src = '';
                analysisResults.innerHTML = '';
                currentImagePath = null;
            }
        });
    });
});
// Ensure page loads at the top
window.onload = function () {
    window.scrollTo(0, 0);
};

document.addEventListener('DOMContentLoaded', function () {
    const maxLines = 50;
    enforceLineLimit(document.getElementById("recipients"), maxLines);
    enforceLineLimit(document.getElementById("recipient_names"), maxLines);
    enforceLineLimit(document.getElementById("recipient_companies"), maxLines);

    document.getElementById('emailForm').addEventListener('submit', function(event) {
        event.preventDefault();  // Prevents default submission
        sendingemail();
    });

    // Add button click event listeners here
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function() {
            this.classList.add('loading');
            setTimeout(() => {
                this.classList.remove('loading'); // Remove loading class after task
            }, 2000); // Adjust the timeout as needed
        });
    });
});

function sendingemail() {
    const messageBox = document.getElementById('message');
    const subjectBox = document.getElementById('subject');

    // Check if the elements exist
    if (!messageBox || !subjectBox) {
        console.error('Message box or subject box not found.');
        return; // Exit the function if elements are not found
    }

    // Get the current content of the message and subject
    let messageContent = messageBox.innerHTML || ''; // Fallback to empty string
    let subjectContent = subjectBox.innerHTML || ''; // Use innerHTML for contenteditable div

    // Log the contents for debugging
    console.log('Message Content:', messageContent);
    console.log('Subject Content:', subjectContent);

    // Step 1: Replace placeholder images with text placeholders in both message and subject
    messageContent = messageContent.replace(/<img[^>]*src="\/static\/recipientname\.png"[^>]*>/g, '|recipient name|');
    messageContent = messageContent.replace(/<img[^>]*src="\/static\/companyname\.png"[^>]*>/g, '|recipient company|');

    subjectContent = subjectContent.replace(/<img[^>]*src="\/static\/recipientname\.png"[^>]*>/g, '|recipient name|');
    subjectContent = subjectContent.replace(/<img[^>]*src="\/static\/companyname\.png"[^>]*>/g, '|recipient company|');

    // Step 2: Clean up HTML tags in message content
    messageContent = messageContent.replace(/<div>/g, ''); // Remove opening <div> tags
    messageContent = messageContent.replace(/<\/div>/g, '\n'); // Replace closing </div> tags with line breaks
    messageContent = messageContent.replace(/<br\s*\/?>/g, '\n'); // Replace <br> tags with line breaks
    messageContent = messageContent.replace(/&quot;/g, '"'); // Replace HTML entity for quotes with actual quotes

    // Clean up HTML tags in subject content
    subjectContent = subjectContent.replace(/<br\s*\/?>/g, '\n'); // Replace <br> tags with new lines
    subjectContent = subjectContent.replace(/<div>/g, ''); // Remove opening <div> tags
    subjectContent = subjectContent.replace(/<\/div>/g, ''); // Remove closing </div> tags
    subjectContent = subjectContent.replace(/&amp;/g, '&'); // Decode &amp; to &
    subjectContent = subjectContent.replace(/&nbsp;/g, ' '); // Replace &nbsp; with a regular space
    subjectContent = subjectContent.replace(/&quot;/g, '"'); // Replace &quot; with actual quotes

    // Update the hidden textarea with the current message content
    document.getElementById('message-content').value = messageContent; 

    // Update the hidden textarea for the subject
    document.getElementById('subject-content').value = subjectContent; // Populate hidden textarea for subject

    // Collect form data
    const emailForm = document.getElementById('emailForm');
    const formData = new FormData(emailForm);
    console.log('Submitting form with data:', [...formData.entries()]);  // Debugging check

    // Send data to the server
    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.text();  // Expect HTML response
    })
    .then(html => {
        document.body.innerHTML = html;  // Replace page content with response
        window.scrollTo(0, 0);  // Scroll to the top
    })
    .catch(error => {
        console.error('Error during fetch:', error);
        alert('❌ Error: ' + error.message);
    });
}

// Function to enforce the line limit
function enforceLineLimit(textarea, maxLines) {
    textarea.addEventListener('input', function () {
        const lines = textarea.value.split("\n");
        if (lines.length > maxLines) {
            alert(`You can only enter up to ${maxLines} lines.`);
            textarea.value = lines.slice(0, maxLines).join("\n");
        }
    });
}

// Function to convert images to placeholders
function convertImagesToPlaceholders() {
    const subjectElement = document.getElementById('subject');
    const messageElement = document.getElementById('message');

    // Replace image tags with text placeholders
    subjectElement.innerHTML = subjectElement.innerHTML
        .replace(/<img[^>]*src="\/static\/recipientname\.png"[^>]*>/g, '|recipient name|')
        .replace(/<img[^>]*src="\/static\/companyname\.png"[^>]*>/g, '|recipient company|');

    messageElement.innerHTML = messageElement.innerHTML
        .replace(/<img[^>]*src="\/static\/recipientname\.png"[^>]*>/g, '|recipient name|')
        .replace(/<img[^>]*src="\/static\/companyname\.png"[^>]*>/g, '|recipient company|');
}

// Handle the Enter key event to insert a line break
document.getElementById('message').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);

            // Create a line break element
            const lineBreak = document.createElement('br');
            range.insertNode(lineBreak); // Insert the line break

            // Move the cursor to the right of the line break
            range.setStartAfter(lineBreak);
            range.setEndAfter(lineBreak);
            selection.removeAllRanges(); // Clear the selection
            selection.addRange(range); // Add the new range to the selection
        }
    }
});

// Handle the Enter key event for the subject
document.getElementById('subject').addEventListener('keydown', function(event) {
    if (event.key === 'Enter') {
        event.preventDefault(); // Prevent the default action
        const selection = window.getSelection();
        if (selection.rangeCount > 0) {
            const range = selection.getRangeAt(0);

            // Create a line break element
            const lineBreak = document.createElement('br');
            range.insertNode(lineBreak); // Insert the line break

            // Move the cursor to the right of the line break
            range.setStartAfter(lineBreak);
            range.setEndAfter(lineBreak);
            selection.removeAllRanges(); // Clear the selection
            selection.addRange(range); // Add the new range to the selection
        }
    }
});

// Function to insert placeholders in both subject and message
function insertPlaceholder(placeholder, target) {
    let targetElement = document.getElementById(target);
    if (!targetElement) return;

    let imgTag;
    if (placeholder === 'recipientname') {
        imgTag = '<img src="/static/recipientname.png" alt="Recipient Name" class="placeholder-img" />';
    } else if (placeholder === 'companyname') {
        imgTag = '<img src="/static/companyname.png" alt="Company Name" class="placeholder-img" />';
    } else {
        return; // If the placeholder is not recognized, exit the function
    }

    // Insert at cursor position
    const selection = window.getSelection();
    if (selection.rangeCount > 0) {
        const range = selection.getRangeAt(0);
        range.deleteContents(); // Remove any selected text

        // Create the image element from the string
        const imgElement = new DOMParser().parseFromString(imgTag, 'text/html').body.firstChild;
        
        // Make image removable when clicked
        imgElement.addEventListener('click', function() {
            imgElement.remove();
        });

        // Insert the image at the cursor
        range.insertNode(imgElement);

        // Move the cursor after the image
        range.setStartAfter(imgElement);
        range.setEndAfter(imgElement);
        selection.removeAllRanges();
        selection.addRange(range);
    } else {
        targetElement.innerHTML += imgTag; // Fallback: Append to the end
    }

    targetElement.focus();
}

// Function to handle spelling correction
function spelling_corrector() {
    const messageDiv = document.getElementById('message');
    let originalHTML = messageDiv.innerHTML; 

    // Step 1: Convert images to text placeholders
    originalHTML = originalHTML.replace(/<img[^>]*src="\/static\/recipientname\.png"[^>]*>/g, '|recipient name|');
    originalHTML = originalHTML.replace(/<img[^>]*src="\/static\/companyname\.png"[^>]*>/g, '|recipient company|');

    // Step 2: Send modified text (with placeholders) to the backend
    fetch('/spelling_correction', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: originalHTML }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // Debugging: log the response data
        if (data.corrected_text) {
            let correctedText = data.corrected_text;

            // Step 3: Reconstruct the message by converting placeholders back to images
            correctedText = correctedText.replace(/\|recipient name\|/g, '<img src="/static/recipientname.png" alt="Recipient Name" class="placeholder-img" />');
            correctedText = correctedText.replace(/\|recipient company\|/g, '<img src="/static/companyname.png" alt="Company Name" class="placeholder-img" />');

            // Step 4: Update the message box with the final corrected text
            messageDiv.innerHTML = correctedText;

            // Step 5: Store the correct message (with images) in the hidden textarea for form submission
            document.getElementById('message-content').value = correctedText;

            // Display changed words (excluding protected tokens)
            const textChanges = data.changed_words.filter(([original, corrected]) => {
                return !['img', 'src', 'png'].includes(original.toLowerCase());
            });

            console.log('Text changes:', textChanges); // Debugging: log the text changes
            document.getElementById('changed-words').textContent = textChanges.length
                ? `Changed words: ${textChanges.map(([original, corrected]) => `${original} → ${corrected}`).join(', ')}`
                : 'No words were changed.';
        } else {
            alert('Error correcting spelling: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => alert('Error correcting spelling: ' + error.message));
}

function reconstructMessage() {
    const messageBox = document.getElementById('message');
    let htmlContent = messageBox.innerHTML;

    // Replace text placeholders with image tags
    htmlContent = htmlContent.replace(/\|recipient name\|/g, '<img src="path/to/recipientname.png" alt="Recipient Name" class="placeholder-img" />');
    htmlContent = htmlContent.replace(/\|recipient company\|/g, '<img src="path/to/companyname.png" alt="Company Name" class="placeholder-img" />');

    messageBox.innerHTML = htmlContent; // Update the message box with the new content
}

// Function to handle spam detection
function spam_detection() {
    const message = document.getElementById('message').value;
    const subject = document.getElementById('subject').value;
    
    fetch('/spam_detection', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: subject + ' ' + message }),
    })
    .then(response => response.json())
    .then(data => {
        document.getElementById('spam-result').textContent = data.is_spam 
            ? 'This message is likely SPAM.' 
            : 'This message is NOT SPAM.';
    })
    .catch(error => document.getElementById('spam-result').textContent = 'Error detecting spam: ' + error.message);
}

 // Tooltip functionality for buttons
const buttons = document.querySelectorAll('.btn');
buttons.forEach(button => {
    // No tooltip logic needed here
});

// Function to simulate a task and toggle loading state
function simulateTask(buttonClass) {
    const button = document.querySelector(`.${buttonClass}`);
    button.classList.add('loading'); // Add loading class
    button.disabled = true; // Disable the button to prevent multiple clicks

    // Simulate an asynchronous task (like sending an email)
    setTimeout(() => {
        // Task is complete, revert button state
        button.classList.remove('loading');
        button.disabled = false; // Re-enable the button
    }, 3000); // Simulate a 3-second task
}

// Attach event listeners to buttons
document.querySelector('.spelling-corrector').addEventListener('click', () => simulateTask('spelling-corrector'));
document.querySelector('.spam-detection').addEventListener('click', () => simulateTask('spam-detection'));
document.querySelector('.send-email').addEventListener('click', () => simulateTask('send-email'));
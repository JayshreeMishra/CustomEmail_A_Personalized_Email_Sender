document.addEventListener('DOMContentLoaded', function () {
    const maxLines = 50;
    enforceLineLimit(document.getElementById("recipients"), maxLines);
    enforceLineLimit(document.getElementById("recipient_names"), maxLines);
    enforceLineLimit(document.getElementById("recipient_companies"), maxLines);
});

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

// Function to insert placeholders into the message box
function insertPlaceholder(placeholder) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;

    const cursorPosition = messageBox.selectionStart;
    const textBeforeCursor = messageBox.value.slice(0, cursorPosition);
    const textAfterCursor = messageBox.value.slice(cursorPosition);

    messageBox.value = `${textBeforeCursor}|${placeholder}|${textAfterCursor}`;
    messageBox.selectionStart = messageBox.selectionEnd = cursorPosition + placeholder.length + 2;
    messageBox.focus();
}

// Function to handle spelling correction
function correctSpelling() {
    const message = document.getElementById('message').value;
    fetch('/correct_spelling', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.corrected_text) {
            document.getElementById('message').value = data.corrected_text;
            document.getElementById('changed-words').textContent = data.changed_words.length
                ? `Changed words: ${data.changed_words.map(([original, corrected]) => `${original} → ${corrected}`).join(', ')}`
                : 'No words were changed.';
        } else {
            alert('Error correcting spelling: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => alert('Error correcting spelling: ' + error.message));
}

// Function to handle spam detection
function detectSpam() {
    const message = document.getElementById('message').value;
    const subject = document.getElementById('subject').value;
    
    fetch('/detect_spam', {
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

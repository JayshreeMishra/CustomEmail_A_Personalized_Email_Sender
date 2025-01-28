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

// Apply the line limit enforcement on page load
document.addEventListener('DOMContentLoaded', function () {
    const maxLines = 50;
    const recipientsTextarea = document.getElementsByName("recipients")[0];
    const recipientNamesTextarea = document.getElementsByName("recipient_names")[0];
    const recipientCompaniesTextarea = document.getElementsByName("recipient_companies")[0];

    enforceLineLimit(recipientsTextarea, maxLines);
    enforceLineLimit(recipientNamesTextarea, maxLines);
    enforceLineLimit(recipientCompaniesTextarea, maxLines);
});

// Function to insert placeholders into the message box
function insertPlaceholder(placeholder) {
    console.log(`Inserting placeholder: ${placeholder}`);
    const messageBox = document.getElementById('message');
    if (!messageBox) return;

    const cursorPosition = messageBox.selectionStart; // Get cursor position
    const textBeforeCursor = messageBox.value.slice(0, cursorPosition);
    const textAfterCursor = messageBox.value.slice(cursorPosition);

    // Insert the placeholder at the cursor position
    messageBox.value = `${textBeforeCursor}|${placeholder}|${textAfterCursor}`;

    // Move the cursor to after the inserted placeholder
    const newCursorPosition = cursorPosition + placeholder.length + 2; // 2 for the surrounding pipes
    messageBox.selectionStart = messageBox.selectionEnd = newCursorPosition;

    // Focus back on the message box
    messageBox.focus();
}

// Function to handle spelling correction
function correctSpelling() {
    const message = document.getElementById('message').value;
    fetch('/correct_spelling', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: message }),
    })
    .then(response => response.json())
    .then(data => {
        if (data.corrected_text) {
            // Update the message textarea with the corrected text
            document.getElementById('message').value = data.corrected_text;

            // Display the changed words
            const changedWordsDiv = document.getElementById('changed-words');
            if (data.changed_words && data.changed_words.length > 0) {
                // Create a list of changed words
                const changedWordsList = data.changed_words.map(([original, corrected]) => 
                    `${original} → ${corrected}`
                ).join(', ');

                // Display the list
                changedWordsDiv.textContent = `Changed words: ${changedWordsList}`;
                changedWordsDiv.style.color = 'green'; // Set color to green
            } else {
                // No words were changed
                changedWordsDiv.textContent = 'No words were changed.';
                changedWordsDiv.style.color = 'gray'; // Set color to gray
            }
        } else {
            alert('Error correcting spelling: ' + (data.error || 'Unknown error'));
        }
    })
    .catch(error => {
        alert('Error correcting spelling: ' + error.message);
    });
}

// Function to handle spam detection
function detectSpam() {
    const message = document.getElementById('message').value;
    const subject = document.getElementsByName('subject')[0].value;
    const combinedText = subject + ' ' + message;

    fetch('/detect_spam', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ text: combinedText }),
    })
    .then(response => response.json())
    .then(data => {
        const resultDiv = document.getElementById('spam-result');
        if (data.is_spam !== undefined) {
            resultDiv.textContent = data.is_spam ? 'This message is likely SPAM.' : 'This message is NOT SPAM.';
        } else {
            resultDiv.textContent = 'Error detecting spam: ' + (data.error || 'Unknown error');
        }
    })
    .catch(error => {
        document.getElementById('spam-result').textContent = 'Error detecting spam: ' + error.message;
    });
}
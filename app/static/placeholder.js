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

function updateMessageContent() {
    const messageDiv = document.getElementById('message');
    const messageTextarea = document.getElementById('message-content');

    // Update the hidden textarea with the content of the editable div
    messageTextarea.value = messageDiv.innerHTML;
}

function insertPlaceholder(placeholder) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;

    // Create an image element
    const img = document.createElement('img');
    img.src = `/static/${placeholder.toLowerCase()}.png`;
    img.alt = placeholder;
    img.title = placeholder;
    img.className = 'placeholder-icon';

    // Insert the image at the cursor position
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    range.deleteContents();
    range.insertNode(img);

    // Move cursor after the inserted image
    range.setStartAfter(img);
    range.setEndAfter(img);
    selection.removeAllRanges();
    selection.addRange(range);
}

// Function to handle spelling correction
function spelling_corrector() {
    const message = document.getElementById('message').value;
    fetch('/spelling_correction', {
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
      const tooltipText = button.getAttribute('data-tooltip');
      if (tooltipText) {
          button.addEventListener('mouseenter', () => {
              const tooltip = document.createElement('span');
              tooltip.className = 'button-tooltip';
              tooltip.textContent = tooltipText;
              button.appendChild(tooltip);
          });
          button.addEventListener('mouseleave', () => {
              const tooltip = button.querySelector('.button-tooltip');
              if (tooltip) {
                  tooltip.remove();
              }
          });
      }
  });

  function insertPlaceholder(placeholder) {
    const messageBox = document.getElementById('message');
    if (!messageBox) return;

    // Create an image element
    const img = document.createElement('img');
    img.src = `/static/${placeholder}.png`; // Use the placeholder name directly
    img.alt = placeholder;
    img.className = 'placeholder-image';

    // Insert the image at the cursor position
    const selection = window.getSelection();
    const range = selection.getRangeAt(0);
    range.deleteContents();
    range.insertNode(img);

    // Move cursor after the inserted image
    range.setStartAfter(img);
    range.setEndAfter(img);
    selection.removeAllRanges();
    selection.addRange(range);
}

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

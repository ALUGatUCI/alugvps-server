window.onload = function() {
    const input = document.getElementById('answer');
    input.addEventListener('input', countChars);
}

function countChars() {
    const input = document.getElementById('answer');
    const charCount = document.getElementById('counter');
    charCount.textContent = `Characters (300 minimum): ${input.value.length}`;
}
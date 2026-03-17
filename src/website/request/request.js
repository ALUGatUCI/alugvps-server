window.onload = function() {
    const input = document.getElementById('answer');
    input.addEventListener('input', countChars);

    const submit = document.getElementById('submit');
    submit.addEventListener('click', submitRequest);
}

function countChars() {
    const input = document.getElementById('answer');
    const charCount = document.getElementById('counter');
    charCount.textContent = `Characters (300 minimum): ${input.value.length}`;
}

function submitRequest() {
    const answer = document.getElementById('answer').value;
    if (answer.length < 300) {
        alert('Please provide a more detailed answer (at least 300 characters).');
        return;
    }

    fetch('/accounts/request_container', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
        },
        body: JSON.stringify({ request_body: answer })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert('Your request has been submitted successfully! You will receive an email if we approve your request.');
            window.location.href = 'dashboard.html';
        } else {
            alert('There was an error submitting your request: ' + (data.detail || 'Unknown error'));
        }
    })
}
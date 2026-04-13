window.onload = function() {
    validateLogin();

    const input = document.getElementById('answer');
    input.addEventListener('input', countChars);

    const submit = document.getElementById('submit');
    submit.addEventListener('click', submitRequest);

    const logoutButton = document.getElementById('logout');
    logoutButton.onclick = logoutButtonFunc
}

function countChars() {
    const input = document.getElementById('answer');
    const charCount = document.getElementById('counter');
    charCount.textContent = `Characters (300 minimum): ${input.value.length}`;
}

async function submitRequest() {
    const answer = document.getElementById('answer').value;
    if (answer.length < 300) {
        alert('Please provide a more detailed answer (at least 300 characters).');
        return;
    }


    if (confirm("Are you sure you want to submit your application? You will not be able to make any changes once you submit it.")) {
        const request = await fetch('/accounts/request_container', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`,
            },
            body: JSON.stringify({ 'request_body': answer })
        })

        if (request.ok) {
            alert("Your request has been successfully submitted. You will receive an email when we approve your request.")
        } else {
            const errorData = await request.json();
            alert(`An error occurred submitting your request: ${errorData.detail}`)
        }
    }
}
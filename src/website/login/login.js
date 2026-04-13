window.onload = function() {
    validateLogin();

    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        // Check the token is still valid
        fetch('/accounts/verify_token', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${accessToken}`
        }
    }).then(response => {
        if (response.status === 200) {
            // Check if the token is valid by making a request to a protected endpoint
            redirectToDashboard();
        } else {
            localStorage.removeItem('access_token');
        }
    }).catch(error => {
        console.alert(`There was an error validating your token: ${error}`)
        localStorage.removeItem('access_token');
    })
    };
    loginButton.addEventListener('click', async () => {
        await login();
    });
}

async function login() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Send the login request to the server
    const data = await fetch(`/token`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded'
        },
        body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
    })

    if (data.access_token) {
        // Store the access token in local storage
        localStorage.setItem('access_token', data.access_token);
        alert('Login successful!');
        // Redirect to the dashboard or another page
        redirectToDashboard();
    } else {
        alert('Login failed: ' + (data.detail || 'Unknown error'));
    }
}
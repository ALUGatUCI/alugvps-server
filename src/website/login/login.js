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

    try {
        // Send the login request to the server
        fetch(`/token`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            body: `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`
        })
        .then(response => response.json())
        .then(data => {
            if (data.access_token) {
                // Store the access token in local storage
                localStorage.setItem('access_token', data.access_token);
                alert('Login successful!');
                // Redirect to the dashboard or another page
                redirectToDashboard();
            } else {
                alert('Login failed: ' + (data.detail || 'Unknown error'));
            }
        })
    } catch (error) {
        console.error('Login error:', error);
        alert('An error occurred during login. Please try again.');
    }
}

function redirectToDashboard() {
    if (fetch('/containers/exists').then(res => res.json()).then(existsData => existsData.exists)) {
        window.location.href = 'dashboard.html';
    } else {
        window.location.href = 'request.html';
    }
}
function validateLogin() {
    // Automatically redirect to login if access token exists and is not valid
    const accessToken = localStorage.getItem('access_token');

    if (!accessToken) {
        if (!window.location.href.endsWith('index.html')) {
            window.location.href = 'index.html';
        }
    }

    // Check if the token is valid by making a request to a protected endpoint
    fetch('/accounts/verify_token', {
        method: 'GET',
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${accessToken}`
        }
    }).then(response => {
        if (response.status === 401) {
            localStorage.removeItem('access_token');
            if (!window.location.href.endsWith('index.html')) {
                window.location.href = 'index.html';
            }
        } else {
            redirectToDashboard();
        }
    }).catch(error => {
        console.error('Error verifying token:', error);
        // If there's an error (e.g., token is invalid), redirect to login
        localStorage.removeItem('access_token');
        window.location.href = 'index.html';
    });

    // Load the Ubuntu font from Google Fonts
    const preconnectAPI = document.createElement('link');
    preconnectAPI.rel = 'preconnect';
    preconnectAPI.href = 'https://fonts.googleapis.com';
    preconnectAPI.crossOrigin = 'anonymous';
    document.head.appendChild(preconnectAPI);

    const preconnectFonts = document.createElement('link');
    preconnectFonts.rel = 'preconnect';
    preconnectFonts.href = 'https://fonts.gstatic.com';
    preconnectFonts.crossOrigin = 'anonymous';
    document.head.appendChild(preconnectFonts);

    const font = document.createElement('link');
    font.href = 'https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap';
    font.rel = 'stylesheet';
    document.head.appendChild(font);
}

async function redirectToDashboard() {
    const accessToken = localStorage.getItem('access_token');

    const apiCall = await fetch('/accounts/account_confirmed', {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${accessToken}`
        }
    });
    const result = await apiCall.json();

    if (result.confirmed) {
        const confirmed = await fetch('/containers/exists', {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
                'Authorization': `Bearer ${accessToken}`
            }
        });
        if (confirmed.ok) {
            const data = confirmed.json();
            if (data.exists) {
                if (!window.location.href.endsWith('dashboard.html')) {
                    window.location.href = 'dashboard.html';
                }
            } else {
                if (!window.location.href.endsWith('request.html')) {
                    window.location.href = 'request.html';
                }
            }
        }
    } else {
        if (!window.location.href.endsWith('confirm.html')) {
            window.location.href = 'confirm.html';
        }
    }
}

// This is for logout buttons
async function logoutButtonFunc() {
    const response = await fetch('/accounts/logout', {
        method: 'POST',
        headers: {
            "Content-Type": "application/json",
            'Authorization': `Bearer ${localStorage.getItem("access_token")}`,
        }
    });

    if (response.ok) {
        alert("Logged out successfully");
        window.location.reload()
    } else {
        const errorData = await response.json()
        alert(`An error occurred logging you out: ${errorData.detail}`)
    }
}
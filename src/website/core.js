window.onload = function() {
    // Automatically redirect to login if access token exists and is not valid
    const accessToken = localStorage.getItem('access_token');
    if (accessToken) {
        // Check if the token is valid by making a request to a protected endpoint
        fetch('/accounts/verify_token', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`
            }
        })
        .then(response => function() {
            if (response.status === 200) {
                redirectToDashboard();
            } else {
                localStorage.removeItem('access_token');
                window.location.href = 'index.html';
            }
        })
    }

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

    const loginButton = document.getElementById('loginButton');
}
window.onload = function() {
    const startButton = document.getElementById('start').addEventListener('click', startVPS);
    const stopButton = document.getElementById('stop').addEventListener('click', stopVPS);
    const rebootButton = document.getElementById('reboot').addEventListener('click', rebootVPS);
    const sshAddressSpan = document.getElementById('sshAddress');
    
    setContainerStatus(); // Initial fetch of container status
    setInterval(setContainerStatus, 1500); // Update container status every 1.5 seconds
}

function setContainerStatus() {
    const containerStatusSpan = document.getElementById('containerStatus')

    // Fetch the container status on page load
    fetch('/containers/status', {
        method: 'GET',
        headers: {
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            containerStatusSpan.textContent = data.status;
        } else {
            containerStatusSpan.textContent = 'Unknown';
        }
    }).catch(error => {
        console.error('Error fetching container status:', error);
        containerStatusSpan.textContent = 'Unknown';
    });
}

function startVPS() {
    fetch('/containers/start', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('VPS started successfully!');
        } else {
            alert('Failed to start VPS: ' + data.message);
        }
    }).catch(error => {
        console.error('Error starting VPS:', error);
        alert('Failed to start VPS: ' + (error.message || 'Unknown error'));
    })
}

function stopVPS() {
    fetch('/containers/stop', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('VPS stopped successfully!');
        } else {
            alert('Failed to stop VPS: ' + data.message);
        }
    }).catch(error => {
        console.error('Error stopping VPS:', error);
        alert('Failed to stop VPS: ' + (error.message || 'Unknown error'));
    })
}

function rebootVPS() {
    fetch('/containers/restart', {
        method: 'PUT',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert('VPS rebooted successfully!');
        } else {
            alert('Failed to reboot VPS: ' + data.message);
        }
    }).catch(error => {
        console.error('Error rebooting VPS:', error);
        alert('Failed to reboot VPS: ' + (error.message || 'Unknown error'));
    })
}
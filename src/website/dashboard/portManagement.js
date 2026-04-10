export async function savePort(portName, listen, connect) {
    const params = new URLSearchParams({'name': portName, 'listen': listen, 'connect': connect});
    return fetch(`/containers/port/add?${params}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },

    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("The port has successfully be submitted");
        } else {
            alert(`An issue occurred submitting the port: ${data.message}`)
        }
    })
    .catch(error => {
        alert(`An error occurred trying to submit the port: ${error}`)
    })
}
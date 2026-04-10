export function savePort(portName, listen, connect) {
    fetch("/containers/port/add", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        },
        body: JSON.stringify({'name': portName, 'listen': listen, 'connect': connect})

    })
    .then(response => {
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("The port has successfully be submitted");
        }
    })
    .catch(error => {
        alert(`An error occurred trying to submit the port: ${error}`)
    })
}
function getLocationAndSendToFlask() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(success, error, { timeout: 10000 });
    } else {
        window.location.href = "/"; 
    }
}

function success(position) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
        .then(response => response.json())
        .then(data => {
            const state = data.address.state;
            const city = data.address.city || data.address.town || "Unknown"; // Handle cases where city might not be present
            const pincode = data.address.postcode;
            sendStateToFlask(city, state, lat, lng, pincode);
        })
        .catch(() => window.location.href = "/"); 
}

function error() {
    window.location.href = "/";
}

function sendStateToFlask(city, state, lat, lng, pincode) {
    // Prepare the data to send
    const data = {
        city: city,
        state: state,
        latitude: lat,
        longitude: lng,
        pincode: pincode
    };

    // Send a POST request to the Flask server
    fetch('/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(data)  // Send the data as JSON
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // You can handle the response here if needed
        console.log('Data sent successfully:', data);
    })
    .catch(error => {
        console.error('There was a problem with the fetch operation:', error);
    });
}


window.onload = getLocationAndSendToFlask;

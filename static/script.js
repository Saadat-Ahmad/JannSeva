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
            sendStateToFlask(state);
        })
        .catch(() => window.location.href = "/"); 
}

function error() {
    window.location.href = "/";
}

function sendStateToFlask(state) {
    fetch("/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ state: state }),
    })
    .then(response => response.text())
    .then(html => {
        document.open();
        document.write(html);
        document.close();
    });
}

window.onload = getLocationAndSendToFlask;

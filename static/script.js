function handleSubmit(event) {
    event.preventDefault();
    const textInput = document.getElementById('text_input').value;
    
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            position => success(position, textInput),
            error => fallbackSend(textInput),
            { timeout: 10000 }
        );
    } else {
        fallbackSend(textInput);
    }
}

function success(position, textInput) {
    const lat = position.coords.latitude;
    const lng = position.coords.longitude;

    fetch(`https://nominatim.openstreetmap.org/reverse?lat=${lat}&lon=${lng}&format=json`)
        .then(response => response.json())
        .then(data => {
            const address = data.address || {};
            const formData = {
                text_input: textInput,
                city: address.city || address.town || "Unknown",
                state: address.state,
                latitude: lat,
                longitude: lng,
                pincode: address.postcode
            };
            sendToFlask(formData);
        })
        .catch(() => fallbackSend(textInput));
}

function fallbackSend(textInput) {
    sendToFlask({
        text_input: textInput,
        city: "Unknown",
        state: "Unknown",
        latitude: null,
        longitude: null,
        pincode: null
    });
}

function sendToFlask(data) {
    const formData = new FormData();
    for (const key in data) {
        formData.append(key, data[key]);
    }

    fetch('/', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json()) // Parse the JSON response
    .then(responseData => {
        // Update the chat box with the bot's response
        const chatBox = document.getElementById('chat-box');
        const userMessage = document.createElement('div');
        userMessage.className = 'message user';
        userMessage.textContent = data.text_input; // Show the user's input
        chatBox.appendChild(userMessage);

        const botMessage = document.createElement('div');
        botMessage.className = 'message bot';
        botMessage.textContent = responseData.response; // Show the bot's response
        chatBox.appendChild(botMessage);

        // Scroll to the bottom of the chat box
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(error => console.error('Error:', error));
}
// Remove the window.onload geolocation call
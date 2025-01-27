// Access webcam
const video = document.getElementById('webcam');
const emotionLabel = document.getElementById('emotion');
const confidenceLabel = document.getElementById('confidence');

// Start webcam
navigator.mediaDevices.getUserMedia({ video: true })
    .then((stream) => {
        video.srcObject = stream;
    })
    .catch((err) => {
        console.error("Error accessing webcam: ", err);
    });

// Capture frame from webcam every 100ms
setInterval(() => {
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Convert the frame to a base64 string
    const frameData = canvas.toDataURL('image/jpeg');

    // Send the frame to the backend
    fetch('/process_frame', {
        method: 'POST',
        body: new URLSearchParams({ frame_data: frameData }),
    })
    .then((response) => response.json())
    .then((data) => {
        emotionLabel.textContent = `Emotion: ${data.emotion}`;
        confidenceLabel.textContent = `Confidence: ${data.confidence}%`;
    })
    .catch((error) => {
        console.error('Error:', error);
    });
}, 100); // Capture frame every 100ms

// userMovement.js

// Get the video element for the camera feed
const cameraFeed = document.getElementById('camera-feed');

// Check if the browser supports accessing the camera
if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            // Set the source of the video element to the camera stream
            cameraFeed.srcObject = stream;
        })
        .catch(function(error) {
            console.error("Error accessing the camera: ", error);
        });
} else {
    alert("Your browser does not support accessing the camera.");
}

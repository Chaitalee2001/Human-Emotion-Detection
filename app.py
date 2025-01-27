from flask import Flask, render_template, Response
import cv2
from deepface import DeepFace
import threading

app = Flask(__name__)

# Initialize webcam
cap = cv2.VideoCapture(0)

# Ensure the webcam is opened
if not cap.isOpened():
    print("Error: Could not open webcam.")
    exit()

# Configure webcam resolution
frame_width = 640
frame_height = 480
cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)

def gen_frames():
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        
        # Resize frame for faster processing
        frame_resized = cv2.resize(frame, (frame_width, frame_height))

        try:
            # Detect emotion using DeepFace
            analysis = DeepFace.analyze(frame_resized, actions=['emotion'], enforce_detection=False)
            dominant_emotion = analysis[0]['dominant_emotion']
            confidence = analysis[0]['emotion'][dominant_emotion]  # Confidence score for the emotion
        except Exception as e:
            dominant_emotion = "Unknown"
            confidence = 0.0

        # Add emotion and confidence to the frame
        cv2.putText(frame_resized, f"Emotion: {dominant_emotion}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame_resized, f"Confidence: {confidence:.2f}%", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # Convert the frame to JPEG
        ret, buffer = cv2.imencode('.jpg', frame_resized)
        if not ret:
            continue
        frame = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(debug=True)

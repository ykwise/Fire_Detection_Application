from flask import Flask, render_template, request, jsonify
from ultralytics import YOLO
from PIL import Image
import io
import time
import os

# 🔽 NEW: Import auto downloader
from download_model import download_model

# Import the notification functions and config variables
from notifications import send_sms_alert, send_email_alert, upload_image_to_cloudinary
import config


# =====================================================
# 🔥 AI MODEL AUTO DOWNLOAD + LOAD (IMPORTANT SECTION)
# =====================================================

MODEL_PATH = "model/best.pt"

# Step 1: Download model automatically if missing
if not os.path.exists(MODEL_PATH):
    print("Custom model not found. Downloading from Google Drive...")
    download_model()

# Step 2: Load the model safely
try:
    model = YOLO(MODEL_PATH)
    print("✅ Custom Fire Detection Model Loaded Successfully!")
except Exception as e:
    print("❌ CRITICAL ERROR: Could not load the YOLOv8 model.")
    print("Details:", e)
    model = None

# =====================================================
# End of AI Model Setup
# =====================================================


# --- Alert Cooldown Logic ---
ALERT_COOLDOWN_SECONDS = 60  # Cooldown set to 1 minute
last_alert_time = 0
# --------------------------


app = Flask(__name__)

@app.route('/')
def index():
    """Renders the homepage."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """Handles image frames from the webcam, runs prediction, and manages alerts."""
    global last_alert_time

    if model is None:
        return jsonify({'error': 'AI model is not loaded.'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part in the request.'}), 400
    
    file = request.files['file']
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    if file:
        # We need to read the file content to use it multiple times
        image_bytes = file.read()
        
        try:
            image = Image.open(io.BytesIO(image_bytes))
            
            # Run YOLOv8 inference on the frame
            results = model(image, verbose=False) 
            
            fire_detected = False
            # Check results for 'fire' or 'smoke' detections
            for r in results:
                for c in r.boxes.cls:
                    class_name = model.names[int(c)]
                    if class_name in ['fire', 'smoke']:
                        fire_detected = True
                        break
                if fire_detected:
                    break
            
            # --- Handle Alerting and Cooldown ---
            if fire_detected:
                if (time.time() - last_alert_time) > ALERT_COOLDOWN_SECONDS:
                    # Cooldown has passed, send alerts
                    print("Fire detected! Sending notifications and uploading image...")
                    
                    # Upload image to Cloudinary and get the URL
                    image_url = upload_image_to_cloudinary(image_bytes)
                    
                    if image_url:
                        print(f"Image uploaded to Cloudinary: {image_url}")
                    
                        # Send alerts and include the image URL
                        sms_status = send_sms_alert(config.TWILIO_RECIPIENT_PHONE, latitude, longitude, image_url)
                        email_status = send_email_alert(config.ALERT_RECIPIENT_EMAIL, latitude, longitude, image_url)
                        print(f"SMS Status: {sms_status}")
                        print(f"Email Status: {email_status}")
                    else:
                        print("Failed to upload image to Cloudinary. Sending alerts without image URL.")
                        # Send alerts without the image URL as a fallback
                        sms_status = send_sms_alert(config.TWILIO_RECIPIENT_PHONE, latitude, longitude, None)
                        email_status = send_email_alert(config.ALERT_RECIPIENT_EMAIL, latitude, longitude, None)
                        print(f"SMS Status: {sms_status}")
                        print(f"Email Status: {email_status}")


                    last_alert_time = time.time()  # Reset the timer
                    return jsonify({'status': 'alert_sent'})
                else:
                    # Still in cooldown
                    print("Fire detected, but still in cooldown period.")
                    return jsonify({'status': 'cooldown'})
            else:
                return jsonify({'status': 'no_fire'})

        except Exception as e:
            print(f"Error during prediction: {e}")
            return jsonify({'error': str(e)}), 500

    return jsonify({'error': 'No file received.'}), 400


# This block of code allows us to run the app directly
if __name__ == '__main__':
    app.run(debug=True)


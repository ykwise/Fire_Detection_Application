# =========================================================
# 🔥 NOTIFICATIONS MODULE (FINAL VERSION)
# =========================================================

import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

from twilio.rest import Client
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import cloudinary
import cloudinary.uploader

# =========================================================
# ☁️ CLOUDINARY CONFIG (using CLOUDINARY_URL)
# =========================================================
cloudinary.config(
    cloudinary_url=os.getenv("CLOUDINARY_URL"),
    secure=True
)

# =========================================================
# 📱 TWILIO CONFIG
# =========================================================
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")

# =========================================================
# 📧 SENDGRID CONFIG
# =========================================================
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")


# =========================================================
# 📸 Upload Image to Cloudinary
# =========================================================
def upload_image_to_cloudinary(image_bytes):
    try:
        print("Uploading image to Cloudinary...")

        result = cloudinary.uploader.upload(
            image_bytes,
            folder="fire-detection"
        )

        image_url = result.get("secure_url")
        print("Image uploaded successfully:", image_url)

        return image_url

    except Exception as e:
        print("Error uploading to Cloudinary:", e)
        return None


# =========================================================
# 📱 Send SMS Alert
# =========================================================
def send_sms_alert(recipient, latitude, longitude, image_url=None):
    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        body = f"🔥 FIRE ALERT!\n\nLocation: {latitude},{longitude}\nMap: {maps_link}"
        if image_url:
            body += f"\nPhoto: {image_url}"

        message = client.messages.create(
            body=body,
            from_=TWILIO_PHONE_NUMBER,
            to=recipient
        )

        return f"SMS Sent (SID): {message.sid}"

    except Exception as e:
        return f"Error sending SMS: {e}"


# =========================================================
# 📧 Send Email Alert
# =========================================================
def send_email_alert(recipient, latitude, longitude, image_url=None):
    try:
        maps_link = f"https://www.google.com/maps?q={latitude},{longitude}"

        html_content = f"""
        <h1>🔥 Fire Alert Detected</h1>
        <p>Location: {latitude}, {longitude}</p>
        <a href="{maps_link}">View on Google Maps</a>
        """

        if image_url:
            html_content += f"<br><img src='{image_url}' width='400'>"

        message = Mail(
            from_email=SENDER_EMAIL,
            to_emails=recipient,
            subject="🚨 Fire Detected!",
            html_content=html_content
        )

        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.send(message)

        return f"Email Sent (Status Code): {response.status_code}"

    except Exception as e:
        return f"Error sending email: {e}"
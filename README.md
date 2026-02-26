# 🔥 Vision-Based Fire Detection System

A real-time Fire & Smoke Detection Web Application using **YOLOv8**, built with Flask and integrated with:

- 📸 Live Webcam Monitoring
- 🚨 SMS Alerts (Twilio)
- 📧 Email Alerts (SendGrid)
- ☁️ Cloud Image Upload (Cloudinary)
- 📍 GPS Location Sharing
- 🔁 Alert Cooldown Logic
- 🤖 Custom Trained YOLOv8 Model (Auto Download)

---

## 🧠 Project Architecture

User Webcam  
⬇  
Flask Backend  
⬇  
YOLOv8 Custom Model  
⬇  
If Fire Detected:
- Upload Image to Cloudinary
- Send SMS Alert
- Send Email Alert
- Apply Cooldown Timer

---

## 🚀 Features

- Real-time object detection
- Custom-trained fire/smoke model
- Automatic model download on first run
- Secure API key handling using `.env`
- Production-style backend structure

---

# ⚙️ Setup Guide (Works on Any Device)

## 1️⃣ Clone the Repository

```bash
git clone https://github.com/ykwise/Fire_Detection_Application.git
cd Fire_Detection_Application

2️⃣ Create Virtual Environment
Windows
python -m venv venv
venv\Scripts\activate

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Create .env File (IMPORTANT)

Create a file named:

.env

Add your API keys:

TWILIO_ACCOUNT_SID=your_sid
TWILIO_AUTH_TOKEN=your_token
TWILIO_PHONE_NUMBER=your_twilio_number

SENDGRID_API_KEY=your_sendgrid_key
SENDER_EMAIL=your_verified_email

CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

TWILIO_RECIPIENT_PHONE=recipient_phone
ALERT_RECIPIENT_EMAIL=recipient_email

5️⃣ Run the Application
python app.py

Open in browser:

http://127.0.0.1:5000

📦 Tech Stack

Python

Flask

YOLOv8 (Ultralytics)

Twilio API

SendGrid API

Cloudinary

HTML / JavaScript
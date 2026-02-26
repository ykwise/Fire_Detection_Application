import os
import gdown

MODEL_DIR = "model"
MODEL_PATH = os.path.join(MODEL_DIR, "best.pt")

# Your Google Drive file id
FILE_ID = "1Fwo6HSbdnPSph-seik1sVabNLkVFAJ52"

def download_model():
    os.makedirs(MODEL_DIR, exist_ok=True)

    if os.path.exists(MODEL_PATH):
        print("Custom model already exists.")
        return

    print("Downloading custom trained model from Google Drive...")

    url = f"https://drive.google.com/uc?id={FILE_ID}"
    gdown.download(url, MODEL_PATH, quiet=False)

    print("Model downloaded successfully!")
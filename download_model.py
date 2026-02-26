import os
import requests
from tqdm import tqdm

# --- Configuration ---
# This is the direct download link for the model you found on GitHub.
MODEL_URL = "https://raw.githubusercontent.com/Abonia1/YOLOv8-Fire-and-Smoke-Detection/main/yolov8n.pt"
MODEL_DIR = "model"
MODEL_FILENAME = "yolov8n.pt" # The filename from the new link
MODEL_PATH = os.path.join(MODEL_DIR, MODEL_FILENAME)

def download_model():
    """
    Downloads the YOLOv8 model file with a progress bar.
    """
    print("--- Starting AI Model Download (YOLOv8 from user link) ---")
    
    os.makedirs(MODEL_DIR, exist_ok=True)
    
    if os.path.exists(MODEL_PATH):
        print(f"Model already exists at: {MODEL_PATH}")
        return

    print(f"Downloading model from {MODEL_URL}")
    
    try:
        response = requests.get(MODEL_URL, stream=True)
        response.raise_for_status()

        total_size_in_bytes = int(response.headers.get('content-length', 0))
        block_size = 1024

        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        
        with open(MODEL_PATH, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
                
        progress_bar.close()

        if total_size_in_bytes != 0 and progress_bar.n != total_size_in_bytes:
            print("ERROR, something went wrong during download.")
        else:
            print(f"Model downloaded successfully and saved to: {MODEL_PATH}")

    except requests.exceptions.RequestException as e:
        print(f"ERROR: Could not download the model. Please check your internet connection.")
        print(f"Details: {e}")

if __name__ == '__main__':
    download_model()


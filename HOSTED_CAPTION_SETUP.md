# Hosted Image Captioning API Setup Guide

The "Hosted Caption API" feature allows you to offload the heavy image processing (BLIP model) to a remote server. This is useful if:
- You are running the Streamlit app on a laptop with no GPU.
- You don't want to download the 1GB model locally.
- You want faster inference by using a dedicated GPU server (like Google Colab or a cloud VM).

## 1. How it Works
The Streamlit app sends a `POST` request to your provided URL.
- **Payload**: A multipart/form-data request containing the image file under the key `image`.
- **Headers**: Optional `Authorization: Bearer <YOUR_KEY>` if you set an API key.
- **Expected Response**: A JSON object containing `{"caption": "description of image"}` or `{"text": "..."}`.

## 2. Quick Setup (Google Colab / Remote GPU)

You can run this simple API server on any machine with python installed.

### `caption_server.py`

```python
from fastapi import FastAPI, UploadFile, File, Header, HTTPException
import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image
import io
import uvicorn

app = FastAPI()

# Load Model (Global)
print("Loading BLIP model...")
processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)
print(f"Model loaded on {device}")

API_KEY = "secret-123"  # Change this if you want security

@app.post("/caption")
async def generate_caption(image: UploadFile = File(...), authorization: str = Header(None)):
    # 1. Check API Key (Optional)
    if API_KEY and (not authorization or authorization.split(" ")[1] != API_KEY):
        raise HTTPException(status_code=401, detail="Invalid API Key")

    # 2. Read Image
    contents = await image.read()
    raw_image = Image.open(io.BytesIO(contents)).convert('RGB')

    # 3. Generate Caption
    inputs = processor(raw_image, return_tensors="pt").to(device)
    out = model.generate(**inputs, max_new_tokens=50)
    caption = processor.decode(out[0], skip_special_tokens=True)

    return {"caption": caption}

if __name__ == "__main__":
    # Run on port 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

## 3. Deployment Steps

1.  **Install dependencies** on your server:
    ```bash
    pip install fastapi uvicorn torch transformers pillow python-multipart
    ```
2.  **Run the server**:
    ```bash
    python caption_server.py
    ```
3.  **Get the URL**:
    *   If running locally on another port: `http://localhost:8000/caption`
    *   If using **ngrok** (e.g., in Colab): `https://<random-id>.ngrok-free.app/caption`

## 4. Configure Streamlit
1.  Go to the **Chat** page in your app.
2.  Enable **Advanced Image Captioning**.
3.  Open **Hosted Caption API (Alternative)**.
4.  Enter the URL from step 3 (e.g., `http://localhost:8000/caption`).
5.  Enter the API Key (e.g., `secret-123`).

Now, when you upload an image, the app will send it to your server for captioning!

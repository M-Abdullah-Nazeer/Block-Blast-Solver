from fastapi import FastAPI, File, UploadFile
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Backend is running!"}

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Read the image file into memory
    image_bytes = await file.read()
    image = Image.open(io.BytesIO(image_bytes))

    # Convert to OpenCV format
    image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    # Example: Convert image to grayscale (for testing)
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Convert back to PIL Image
    processed_image = Image.fromarray(gray_image)

    # Save or process further (later we'll detect game grid)
    processed_image.save("processed_output.png")

    return {"message": "Image received and processed!"}


from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import cv2
import numpy as np
from PIL import Image
import io

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Adjust if frontend is deployed elsewhere
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

    # Convert to grayscale
    gray_image = cv2.cvtColor(image_cv, cv2.COLOR_BGR2GRAY)

    # Detect edges using Canny
    edges = cv2.Canny(gray_image, 50, 150)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw contours on the original image
    image_with_contours = image_cv.copy()
    cv2.drawContours(image_with_contours, contours, -1, (0, 255, 0), 2)

    # Convert back to PIL Image for easy debugging
    processed_image = Image.fromarray(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
    processed_image.save("grid_detected.png")

    # Extract block positions
    blocks = []
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w > 20 and h > 20:  # Filter small detections
            blocks.append({"x": x, "y": y, "width": w, "height": h})
    
    return {"message": "Grid detected!", "blocks": blocks}

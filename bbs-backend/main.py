# -------------------------- working fine with light blue color----------------------

# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path
    
#     return None

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         return None
    
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Updated HSV range for blue detection
#     lower_blue = np.array([100, 40, 40])  
#     upper_blue = np.array([130, 255, 255])

#     # Create a blue mask
#     mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

#     # Enhance detection using brightness (V) and saturation (S) for blue areas
#     v_channel = hsv[:, :, 2]  # Brightness
#     s_channel = hsv[:, :, 1]  # Saturation

#     blue_threshold = (v_channel > 40) & (s_channel > 40)  # More inclusive range
#     refined_mask_blue = np.where(blue_threshold, mask_blue, 0).astype(np.uint8)

#     # Invert the refined blue mask for filled blocks
#     mask_filled = cv2.bitwise_not(refined_mask_blue)

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_blue = refined_mask_blue[y_start:y_end, x_start:x_end]
#             cell_filled = mask_filled[y_start:y_end, x_start:x_end]

#             # Save debug images
#             debug_blue_path = os.path.join(DEBUG_DIR, f"cell_blue_{row}_{col}.png")
#             debug_filled_path = os.path.join(DEBUG_DIR, f"cell_filled_{row}_{col}.png")
#             cv2.imwrite(debug_blue_path, cell_blue)
#             cv2.imwrite(debug_filled_path, cell_filled)

#             # If a block has more non-blue pixels, it's filled (1); otherwise, it's empty (0)
#             filled = np.count_nonzero(cell_filled) > (cell_size * cell_size * 0.2)
#             row_data.append(1 if filled else 0)
#         board_matrix.append(row_data)

#     return board_matrix

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     cropped_path = crop_board(file_path)
#     if not cropped_path:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)
    
#     board_matrix = process_image(cropped_path)
#     if board_matrix is None:
#         return JSONResponse(content={"error": "Image processing failed"}, status_code=400)
    
#     return {"board_matrix": board_matrix}












# -------------------------------------detects blocks of all colors from board------------------


# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path
    
#     return None

# def process_image(image_path):
#     image = cv2.imread(image_path)
#     if image is None:
#         return None
    
#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Adjusted HSV ranges
#     lower_filled_blue = np.array([110, 130, 60])
#     upper_filled_blue = np.array([120, 160, 80])

#     lower_empty_blue = np.array([110, 100, 30])
#     upper_empty_blue = np.array([120, 130, 60])

#     # Masks for filled and empty blue blocks
#     mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
#     mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

#     # Ensure non-overlapping detection
#     mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_mask = mask_blue[y_start:y_end, x_start:x_end]

#             # Count nonzero pixels (filled block detection)
#             filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#             row_data.append(0 if filled else 1)
#         board_matrix.append(row_data)

#     return board_matrix


# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)
    
#     cropped_path = crop_board(file_path)
#     if not cropped_path:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)
    
#     board_matrix = process_image(cropped_path)
#     if board_matrix is None:
#         return JSONResponse(content={"error": "Image processing failed"}, status_code=400)
    
#     return {"board_matrix": board_matrix}


# -------------------------------------------- croping shapes image----------------------------------------------------


# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path, (x, y, w, h)

#     return None, None  # Return both cropped path and board coordinates


# def process_image(image_path):
#     if not image_path or not os.path.exists(image_path):
#         raise ValueError(f"Invalid image path: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to load image: {image_path}")

#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Adjusted HSV ranges
#     lower_filled_blue = np.array([110, 130, 60])
#     upper_filled_blue = np.array([120, 160, 80])

#     lower_empty_blue = np.array([110, 100, 30])
#     upper_empty_blue = np.array([120, 130, 60])

#     # Masks for filled and empty blue blocks
#     mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
#     mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

#     # Ensure non-overlapping detection
#     mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_mask = mask_blue[y_start:y_end, x_start:x_end]

#             # Count nonzero pixels (filled block detection)
#             filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#             row_data.append(0 if filled else 1)
#         board_matrix.append(row_data)

#     return board_matrix

# def crop_shapes(image_path, board_coords):
#     image = cv2.imread(image_path)
    
#     if board_coords is None or len(board_coords) != 4:
#         raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

#     x, y, w, h = board_coords  # Now safe to unpack
    
#     # Extending height dynamically
#     shape_area_start = y + h  # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(shapes_path, cropped_shapes)
#     return shapes_path

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     # Unpack tuple properly
#     cropped_board_path, board_coords = crop_board(file_path)
    
#     # Ensure board detection succeeded
#     if not cropped_board_path or board_coords is None:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

#     board_matrix = process_image(cropped_board_path)
#     cropped_shapes_path = crop_shapes(file_path, board_coords)

#     return {
#         "cropped_board": cropped_board_path,
#         "cropped_shapes": cropped_shapes_path,
#         "board_matrix": board_matrix
#     }













# ---------------------------------------shapes are detected and saved-----------------------



# import os
# import cv2
# import numpy as np
# import shutil
# from fastapi import FastAPI, UploadFile, File
# from starlette.responses import JSONResponse
# from fastapi.middleware.cors import CORSMiddleware

# UPLOAD_DIR = "uploads"
# CROPPED_DIR = "cropped"
# DEBUG_DIR = "debug_cells"
# SHAPES_DIR = "cropped_shapes"

# os.makedirs(UPLOAD_DIR, exist_ok=True)
# os.makedirs(CROPPED_DIR, exist_ok=True)
# os.makedirs(DEBUG_DIR, exist_ok=True)
# os.makedirs(SHAPES_DIR, exist_ok=True)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["http://localhost:3000"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# def crop_board(image_path):
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
#     edges = cv2.Canny(thresh, 30, 100)
    
#     contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     board_contour = None
#     max_area = 0
    
#     for contour in contours:
#         approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
#         if len(approx) == 4:
#             x, y, w, h = cv2.boundingRect(approx)
#             area = w * h
#             if area > max_area:
#                 max_area = area
#                 board_contour = (x, y, w, h)
    
#     if board_contour:
#         x, y, w, h = board_contour
#         cropped_image = image[y:y+h, x:x+w]
#         cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
#         cv2.imwrite(cropped_path, cropped_image)
#         return cropped_path, (x, y, w, h)

#     return None, None  # Return both cropped path and board coordinates

# def process_image(image_path):
#     if not image_path or not os.path.exists(image_path):
#         raise ValueError(f"Invalid image path: {image_path}")

#     image = cv2.imread(image_path)
#     if image is None:
#         raise ValueError(f"Failed to load image: {image_path}")

#     hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

#     # Adjusted HSV ranges
#     lower_filled_blue = np.array([110, 130, 60])
#     upper_filled_blue = np.array([120, 160, 80])

#     lower_empty_blue = np.array([110, 100, 30])
#     upper_empty_blue = np.array([120, 130, 60])

#     # Masks for filled and empty blue blocks
#     mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
#     mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

#     # Ensure non-overlapping detection
#     mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

#     height, width = image.shape[:2]
#     cell_size = width // 8  # Assuming an 8x8 grid

#     board_matrix = []
#     for row in range(8):
#         row_data = []
#         for col in range(8):
#             x_start, y_start = col * cell_size, row * cell_size
#             x_end, y_end = x_start + cell_size, y_start + cell_size
#             cell_mask = mask_blue[y_start:y_end, x_start:x_end]

#             # Count nonzero pixels (filled block detection)
#             filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#             row_data.append(0 if filled else 1)
#         board_matrix.append(row_data)

#     return board_matrix

# def crop_shapes(image_path, board_coords):
#     image = cv2.imread(image_path)
    
#     if board_coords is None or len(board_coords) != 4:
#         raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

#     x, y, w, h = board_coords  # Now safe to unpack
    
#     # Extending height dynamically
#     shape_area_start = y + h + 30 # Start right after the board
#     shape_area_height = h // 2  # Adjust this if needed
    
#     cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
#     shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
#     cv2.imwrite(shapes_path, cropped_shapes)
#     return shapes_path






# def detect_shapes(image_path, debug=True):
#     # Load image and convert to grayscale
#     image = cv2.imread(image_path)
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
#     # Apply adaptive thresholding for better shape detection
#     thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
#                                    cv2.THRESH_BINARY_INV, 11, 5)

#     # Use morphological closing to merge broken parts of shapes
#     kernel = np.ones((3, 3), np.uint8)
#     thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

#     # Find contours
#     contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#     # Sort contours from left to right
#     contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

#     # Filter out small contours
#     min_area = 100  # Adjusted to detect smaller shapes
#     filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

#     # Directory to save cropped images
#     output_dir = "cropped_shapes"
#     os.makedirs(output_dir, exist_ok=True)

#     shape_paths = []  # List to store cropped image paths

#     for i, contour in enumerate(filtered_contours):
#         x, y, w, h = cv2.boundingRect(contour)

#         # Ensure the bounding box is large enough
#         if w < 10 or h < 10:
#             continue

#         # Crop the shape
#         cropped_shape = image[y:y+h, x:x+w]

#         # Save cropped shape
#         shape_filename = f"{output_dir}/shape_{i}.jpg"
#         cv2.imwrite(shape_filename, cropped_shape)
#         shape_paths.append(shape_filename)

#     # Debugging images
#     if debug:
#         debug_dir = "debug_images"
#         os.makedirs(debug_dir, exist_ok=True)
#         cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

#     return {"shapes": shape_paths}  # Returning JSON-serializable format















# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     file_path = os.path.join(UPLOAD_DIR, file.filename)
#     with open(file_path, "wb") as buffer:
#         shutil.copyfileobj(file.file, buffer)

#     cropped_board_path, board_coords = crop_board(file_path)
    
#     if not cropped_board_path or board_coords is None:
#         return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

#     board_matrix = process_image(cropped_board_path)
#     cropped_shapes_path = crop_shapes(file_path, board_coords)
#     shapes_matrices = detect_shapes(cropped_shapes_path)

#     for i, shape in enumerate(shapes_matrices):
#         print(f"Shape {i+1}:")
#         for row in shape:
#             print(" ".join(map(str, row)))
#         print("\n")

#     return {
#         "cropped_board": cropped_board_path,
#         "cropped_shapes": cropped_shapes_path,
#         "board_matrix": board_matrix,
#         "shapes": shapes_matrices
#     }







# ----------------------debug------------------------




import os
import cv2
import numpy as np
import shutil
from fastapi import FastAPI, UploadFile, File
from starlette.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from scipy.stats import mode
from math import ceil

UPLOAD_DIR = "uploads"
CROPPED_DIR = "cropped"
DEBUG_DIR = "debug_cells"
SHAPES_DIR = "cropped_shapes"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(CROPPED_DIR, exist_ok=True)
os.makedirs(DEBUG_DIR, exist_ok=True)
os.makedirs(SHAPES_DIR, exist_ok=True)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def crop_board(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    edges = cv2.Canny(thresh, 30, 100)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    board_contour = None
    max_area = 0
    
    for contour in contours:
        approx = cv2.approxPolyDP(contour, 0.02 * cv2.arcLength(contour, True), True)
        if len(approx) == 4:
            x, y, w, h = cv2.boundingRect(approx)
            area = w * h
            if area > max_area:
                max_area = area
                board_contour = (x, y, w, h)
    
    if board_contour:
        x, y, w, h = board_contour
        cropped_image = image[y:y+h, x:x+w]
        cropped_path = os.path.join(CROPPED_DIR, os.path.basename(image_path))
        cv2.imwrite(cropped_path, cropped_image)
        return cropped_path, (x, y, w, h)

    return None, None  # Return both cropped path and board coordinates

def process_image(image_path):
    if not image_path or not os.path.exists(image_path):
        raise ValueError(f"Invalid image path: {image_path}")

    image = cv2.imread(image_path)
    if image is None:
        raise ValueError(f"Failed to load image: {image_path}")

    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Adjusted HSV ranges
    lower_filled_blue = np.array([110, 130, 60])
    upper_filled_blue = np.array([120, 160, 80])

    lower_empty_blue = np.array([110, 100, 30])
    upper_empty_blue = np.array([120, 130, 60])

    # Masks for filled and empty blue blocks
    mask_filled_blue = cv2.inRange(hsv, lower_filled_blue, upper_filled_blue)
    mask_empty_blue = cv2.inRange(hsv, lower_empty_blue, upper_empty_blue)

    # Ensure non-overlapping detection
    mask_blue = mask_filled_blue - mask_empty_blue  # Remove empty blocks from filled blocks

    height, width = image.shape[:2]
    cell_size = width // 8  # Assuming an 8x8 grid

    board_matrix = []
    for row in range(8):
        row_data = []
        for col in range(8):
            x_start, y_start = col * cell_size, row * cell_size
            x_end, y_end = x_start + cell_size, y_start + cell_size
            cell_mask = mask_blue[y_start:y_end, x_start:x_end]

            # Count nonzero pixels (filled block detection)
            filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
            row_data.append(0 if filled else 1)
        board_matrix.append(row_data)

    return board_matrix

def crop_shapes(image_path, board_coords):
    image = cv2.imread(image_path)
    
    if board_coords is None or len(board_coords) != 4:
        raise ValueError(f"Expected 4 values in board_coords, got {board_coords}")

    x, y, w, h = board_coords  # Now safe to unpack
    
    # Extending height dynamically
    shape_area_start = y + h + 30 # Start right after the board
    shape_area_height = h // 2  # Adjust this if needed
    
    cropped_shapes = image[shape_area_start:shape_area_start+shape_area_height, x:x+w]
    
    shapes_path = os.path.join(CROPPED_DIR, "cropped_shapes.jpg")
    cv2.imwrite(shapes_path, cropped_shapes)
    return shapes_path






def detect_shapes(image_path, debug=True):
    # Load image and convert to grayscale
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Apply adaptive thresholding for better shape detection
    thresh = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
                                   cv2.THRESH_BINARY_INV, 101, 10)

    # Use morphological closing to merge broken parts of shapes
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

    # Find contours
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Sort contours from left to right
    contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

    # Filter out small contours
    min_area = 100  # Adjusted to detect smaller shapes
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]

    # Directory to save cropped images
    output_dir = "cropped_shapes"
    os.makedirs(output_dir, exist_ok=True)

    shape_paths = []  # List to store cropped image paths

    for i, contour in enumerate(filtered_contours):
        x, y, w, h = cv2.boundingRect(contour)

        # Ensure the bounding box is large enough
        if w < 10 or h < 10:
            continue

        # Crop the shape
        cropped_shape = image[y:y+h, x:x+w]

        # Save cropped shape
        shape_filename = f"{output_dir}/shape_{i}.jpg"
        cv2.imwrite(shape_filename, cropped_shape)
        shape_paths.append(shape_filename)

    # Debugging images
    if debug:
        debug_dir = "debug_images"
        os.makedirs(debug_dir, exist_ok=True)
        cv2.imwrite(f"{debug_dir}/debug_threshold.jpg", thresh)

    return {"shapes": shape_paths}  # Returning JSON-serializable format







# def process_shapes(shape_paths):
#     shape_data = []
    
#     for shape_path in shape_paths:
#         image = cv2.imread(shape_path)
#         gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
#         _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
#         shape_array = np.zeros((8, 8), dtype=int)
        
#         x_min, y_min, x_max, y_max = np.inf, np.inf, 0, 0
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#             x_min, y_min = min(x_min, x), min(y_min, y)
#             x_max, y_max = max(x_max, x + w), max(y_max, y + h)
        
#         shape_width, shape_height = x_max - x_min, y_max - y_min
        
#         # Prevent division errors and ensure proper scaling
#         block_size_x = max(shape_width / 8, 1)
#         block_size_y = max(shape_height / 8, 1)
        
#         for cnt in contours:
#             x, y, w, h = cv2.boundingRect(cnt)
#             grid_x = min(max(int((x - x_min) / block_size_x), 0), 7)
#             grid_y = min(max(int((y - y_min) / block_size_y), 0), 7)
#             shape_array[grid_y, grid_x] = 1
        
#         shape_data.append(shape_array.tolist())
    
#     return shape_data






# def process_cropped_shapes(directory):
#     if not os.path.exists(directory):
#         raise ValueError(f"Directory does not exist: {directory}")
    
#     shape_matrices = {}
    
#     for filename in sorted(os.listdir(directory)):
#         if filename.startswith("shape_") and filename.endswith(".jpg"):
#             image_path = os.path.join(directory, filename)
#             image = cv2.imread(image_path)
#             if image is None:
#                 print(f"Failed to load {filename}")
#                 continue
            
#             hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            
#             # Define HSV range for detecting shape blocks
#             lower_block = np.array([110, 100, 30])  # Adjust as needed
#             upper_block = np.array([120, 160, 80])  # Adjust as needed
            
#             mask = cv2.inRange(hsv, lower_block, upper_block)
            
#             height, width = image.shape[:2]
#             cell_size = width // 8  # Assuming an 8x8 grid per shape
            
#             shape_matrix = []
#             for row in range(8):
#                 row_data = []
#                 for col in range(8):
#                     x_start, y_start = col * cell_size, row * cell_size
#                     x_end, y_end = x_start + cell_size, y_start + cell_size
#                     cell_mask = mask[y_start:y_end, x_start:x_end]
                    
#                     filled = np.count_nonzero(cell_mask) > (cell_size * cell_size * 0.2)
#                     row_data.append(1 if filled else 0)
#                 shape_matrix.append(row_data)
            
#             shape_matrices[filename] = shape_matrix
    
#     return shape_matrices




# ----------- works with simple row shaped images --------

#   def process_cropped_shapes(directory):
#     """
#     Processes each .jpg image in 'directory' and returns a dictionary of:
#       {
#         "filename.jpg": <2D list (grid) of 0/1 for each detected block>
#       }
#     Uses:
#       1) HSV background removal
#       2) Canny edges to highlight boundaries
#       3) Distance transform + Watershed
#       4) Centroid detection + row clustering
#     """
#     results = {}
#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # -- STEP 1: Remove background (HSV threshold) --
#         hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
#         lower_bg = np.array([200, 50, 40], dtype=np.uint8)
#         upper_bg = np.array([240, 100, 100], dtype=np.uint8)
#         bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)  # background in white
#         mask = cv2.bitwise_not(bg_mask)                 # blocks in white

#         # If the mask is empty, skip
#         if cv2.countNonZero(mask) == 0:
#             print(f"No foreground found in {filename}.")
#             continue

#         # Morphological opening to remove small noise
#         kernel = np.ones((3, 3), np.uint8)
#         mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

#         # -- STEP 2: Canny edge detection to highlight internal boundaries --
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         # Adjust these thresholds as needed:
#         edges = cv2.Canny(gray, threshold1=50, threshold2=150)
#         # Keep edges only within the shape (mask)
#         edges_in_shape = cv2.bitwise_and(edges, mask)

#         # Optionally dilate the edges to make them thicker
#         edges_in_shape = cv2.dilate(edges_in_shape, kernel, iterations=1)

#         # Combine edges with mask so edges become "holes" or boundaries in the shape
#         # We invert edges_in_shape so edges become black (0) within the shape
#         edges_inv = cv2.bitwise_not(edges_in_shape)
#         # Now the shape interior is white except for black lines where edges are
#         combined = cv2.bitwise_and(mask, edges_inv)

#         # -- STEP 3: Distance transform + Watershed on combined result --
#         dist = cv2.distanceTransform(combined, cv2.DIST_L2, 5)
#         # Tweak the factor (0.5, 0.6, 0.7) to separate blocks more or less
#         dist_thresh = 0.6 * dist.max()
#         _, sure_fg = cv2.threshold(dist, dist_thresh, 255, 0)
#         sure_fg = np.uint8(sure_fg)

#         # sure_bg by dilating the original mask
#         sure_bg = cv2.dilate(mask, kernel, iterations=3)
#         unknown = cv2.subtract(sure_bg, sure_fg)

#         # Markers for watershed
#         _, markers = cv2.connectedComponents(sure_fg)
#         markers = markers + 1
#         markers[unknown == 255] = 0

#         # Run watershed
#         markers = cv2.watershed(img, markers)

#         # -- STEP 4: Find centroids of each labeled block --
#         block_centroids = []
#         unique_labels = np.unique(markers)
#         for label in unique_labels:
#             # Skip background (label <= 1) and boundary (-1)
#             if label <= 1:
#                 continue

#             label_mask = np.uint8(markers == label)
#             contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#             if not contours:
#                 continue
#             cnt = max(contours, key=cv2.contourArea)
#             M = cv2.moments(cnt)
#             if M["m00"] != 0:
#                 cx = int(M["m10"] / M["m00"])
#                 cy = int(M["m01"] / M["m00"])
#                 block_centroids.append((cx, cy))

#         if not block_centroids:
#             print(f"No blocks detected after watershed in {filename}.")
#             continue

#         # -- STEP 5: Cluster centroids by row to build a grid --
#         block_centroids.sort(key=lambda p: p[1])  # sort by y
#         row_thresh = 20  # vertical tolerance for grouping into rows
#         row_clusters = []
#         for pt in block_centroids:
#             placed = False
#             for cluster in row_clusters:
#                 avg_y = np.mean([p[1] for p in cluster])
#                 if abs(pt[1] - avg_y) < row_thresh:
#                     cluster.append(pt)
#                     placed = True
#                     break
#             if not placed:
#                 row_clusters.append([pt])

#         # Sort each row cluster by x
#         for cluster in row_clusters:
#             cluster.sort(key=lambda p: p[0])

#         n_rows = len(row_clusters)
#         n_cols = max(len(c) for c in row_clusters)
#         grid = [[0]*n_cols for _ in range(n_rows)]
#         for i, cluster in enumerate(row_clusters):
#             for j, pt in enumerate(cluster):
#                 grid[i][j] = 1

#         results[filename] = grid

#     return results



# l shapes and T shapes getting detected perfectly


# def detect_blocks_final_v2(directory):
#     detected_shapes = {}

#     # Debug folder for visualization
#     debug_dir = os.path.join(directory, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)

#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Convert to grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

#         # Find contours
#         contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         # Determine block size based on contours
#         block_size = 40  # Set default, adjust dynamically if needed
#         min_x, min_y, max_x, max_y = np.inf, np.inf, -np.inf, -np.inf

#         for contour in contours:
#             x, y, w, h = cv2.boundingRect(contour)
#             min_x, min_y = min(min_x, x), min(min_y, y)
#             max_x, max_y = max(max_x, x + w), max(max_y, y + h)

#         # Define grid size
#         rows = (max_y - min_y) // block_size + 1
#         cols = (max_x - min_x) // block_size + 1

#         # Create the 2D array
#         shape_array = np.zeros((rows, cols), dtype=int)

#         # Debugging: Draw detected blocks on the image
#         debug_img = img.copy()

#         for contour in contours:
#             x, y, w, h = cv2.boundingRect(contour)
#             row_idx = (y - min_y) // block_size
#             col_idx = (x - min_x) // block_size
#             shape_array[row_idx: row_idx + (h // block_size), col_idx: col_idx + (w // block_size)] = 1

#             # Draw detected blocks (debugging)
#             cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

#         # Save the debugging image
#         debug_img_path = os.path.join(debug_dir, f"debug_{filename}")
#         cv2.imwrite(debug_img_path, debug_img)

#         # Convert numpy array to list for JSON serialization
#         detected_shapes[filename] = shape_array.tolist()

#     return detected_shapes









# All shapes stored perfectly excpet some shapes having light blue and purple color


# def detect_blocks_final_v2(directory):
#     detected_shapes = {}
#     debug_dir = os.path.join(directory, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Preprocess image
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
#         # Apply erosion to separate potentially merged blocks
#         kernel = np.ones((3, 3), np.uint8)
#         eroded = cv2.erode(thresh, kernel, iterations=1)
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Calculate block_size dynamically
#         widths, heights = [], []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             widths.append(w)
#             heights.append(h)

#         block_width = int(mode(widths).mode) if widths else 40  # Removed [0] index
#         block_height = int(mode(heights).mode) if heights else 40  # Removed [0] index
#         block_size = max(block_width, block_height)

#         # Determine grid bounds
#         min_x = min(cv2.boundingRect(c)[0] for c in contours)
#         min_y = min(cv2.boundingRect(c)[1] for c in contours)

#         # Calculate grid dimensions based on max indices
#         max_col, max_row = 0, 0
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             col = (x - min_x) // block_size
#             row = (y - min_y) // block_size
#             num_cols = max(1, w // block_size)
#             num_rows = max(1, h // block_size)
#             max_col = max(max_col, col + num_cols)
#             max_row = max(max_row, row + num_rows)

#         # Initialize grid
#         rows = max_row
#         cols = max_col
#         shape_array = np.zeros((rows, cols), dtype=int)

#         # Populate the grid
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             col = (x - min_x) // block_size
#             row = (y - min_y) // block_size
#             num_cols = max(1, w // block_size)
#             num_rows = max(1, h // block_size)

#             # Split into individual cells
#             for dr in range(num_rows):
#                 for dc in range(num_cols):
#                     current_row = row + dr
#                     current_col = col + dc
#                     if current_row < rows and current_col < cols:
#                         shape_array[current_row, current_col] = 1

#         # Debug visualization
#         debug_img = img.copy()
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

#         detected_shapes[filename] = shape_array.tolist()

#     return detected_shapes






# debugging 1 shape resolved out of 9

# def detect_blocks_final_v1(directory):
#     detected_shapes = {}
#     debug_dir = os.path.join(directory, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Convert to grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

#         # Apply erosion to separate merged blocks
#         kernel = np.ones((3, 3), np.uint8)
#         eroded = cv2.erode(thresh, kernel, iterations=1)

#         # Find contours
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Compute block size dynamically based on detected contours
#         widths, heights = [], []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             widths.append(w)
#             heights.append(h)

#         block_width = int(mode(widths).mode) if widths else 40  
#         block_height = int(mode(heights).mode) if heights else 40  
#         block_size = max(block_width, block_height)

#         # Determine grid bounds
#         min_x = min(cv2.boundingRect(c)[0] for c in contours)
#         min_y = min(cv2.boundingRect(c)[1] for c in contours)

#         # Compute max rows and columns needed
#         max_col, max_row = 0, 0
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             col = (x - min_x) // block_size
#             row = (y - min_y) // block_size
#             num_cols = max(1, w // block_size)
#             num_rows = max(1, h // block_size)
#             max_col = max(max_col, col + num_cols)
#             max_row = max(max_row, row + num_rows)

#         # Initialize grid
#         shape_array = np.zeros((max_row, max_col), dtype=int)

#         # Populate the grid based on contours
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             col = (x - min_x) // block_size
#             row = (y - min_y) // block_size
#             num_cols = max(1, w // block_size)
#             num_rows = max(1, h // block_size)

#             for dr in range(num_rows):
#                 for dc in range(num_cols):
#                     current_row = row + dr
#                     current_col = col + dc
#                     if current_row < max_row and current_col < max_col:
#                         shape_array[current_row, current_col] = 1

#         detected_shapes[filename] = shape_array.tolist()

#     return detected_shapes

# # Define the directory where images are stored
# image_directory = "/mnt/data/"

# # Run the detection function on uploaded images
# detected_shapes_output = detect_blocks_final_v2(image_directory)

# # Return detected shapes
# detected_shapes_output






# 7 shapes resolved 9 new arised


# def detect_blocks_final_v2(directory):
#     detected_shapes = {}
#     debug_dir = os.path.join(directory, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Preprocess image: grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)
        
#         # Apply erosion to separate potentially merged blocks
#         kernel = np.ones((3, 3), np.uint8)
#         eroded = cv2.erode(thresh, kernel, iterations=1)
        
#         # Find contours of the blocks
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Calculate global bounding box for all contours
#         all_x, all_y, all_xw, all_yh = [], [], [], []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             all_x.append(x)
#             all_y.append(y)
#             all_xw.append(x + w)
#             all_yh.append(y + h)
#         global_min_x = min(all_x)
#         global_min_y = min(all_y)
#         global_max_x = max(all_xw)
#         global_max_y = max(all_yh)

#         # Compute block size using median to be robust against slight differences
#         widths = [cv2.boundingRect(c)[2] for c in contours]
#         heights = [cv2.boundingRect(c)[3] for c in contours]
#         block_width = int(np.median(widths))
#         block_height = int(np.median(heights))
#         block_size = max(block_width, block_height)

#         # Compute grid dimensions using the overall bounding box
#         grid_cols = int(round((global_max_x - global_min_x) / block_size))
#         grid_rows = int(round((global_max_y - global_min_y) / block_size))
#         grid_cols = max(1, grid_cols)
#         grid_rows = max(1, grid_rows)

#         # Initialize the grid
#         shape_array = np.zeros((grid_rows, grid_cols), dtype=int)

#         # Populate the grid for each contour using rounded positions
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             # Determine starting grid cell (using rounding)
#             col = int(round((x - global_min_x) / block_size))
#             row = int(round((y - global_min_y) / block_size))
#             # Determine number of cells occupied by the contour
#             num_cols = max(1, int(round(w / block_size)))
#             num_rows = max(1, int(round(h / block_size)))
#             for dr in range(num_rows):
#                 for dc in range(num_cols):
#                     current_row = row + dr
#                     current_col = col + dc
#                     if current_row < grid_rows and current_col < grid_cols:
#                         shape_array[current_row, current_col] = 1

#         # Debug visualization: draw bounding boxes on the original image
#         debug_img = img.copy()
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

#         detected_shapes[filename] = shape_array.tolist()

#     return detected_shapes









# all shapes get detected except purple which can be detected if kernel has 3



# def cluster_coords(coords, threshold):
#     """
#     Group sorted coordinate values into clusters where successive values
#     differ by no more than the threshold. Returns the cluster centers.
#     """
#     coords_sorted = np.sort(coords)
#     clusters = []
#     current_cluster = [coords_sorted[0]]
#     for coord in coords_sorted[1:]:
#         if abs(coord - current_cluster[-1]) <= threshold:
#             current_cluster.append(coord)
#         else:
#             clusters.append(np.mean(current_cluster))
#             current_cluster = [coord]
#     clusters.append(np.mean(current_cluster))
#     return clusters

# def detect_blocks_final_v2(directory):
#     detected_shapes = {}
#     debug_dir = os.path.join(directory, "debug")
#     os.makedirs(debug_dir, exist_ok=True)

#     filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
#     for filename in filenames:
#         img_path = os.path.join(directory, filename)
#         img = cv2.imread(img_path)
#         if img is None:
#             print(f"Failed to load {filename}. Skipping.")
#             continue

#         # Preprocess image: grayscale and threshold
#         gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#         _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

    


#         # Apply erosion to separate merged blocks
#         kernel = np.ones((2, 2), np.uint8)
#         closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
#         eroded = cv2.erode(closed, kernel, iterations=1)

       

#         # Find contours of the blocks
#         contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#         if not contours:
#             detected_shapes[filename] = []
#             continue

#         # Compute centroids for each detected contour
#         centroids = []
#         widths = []
#         heights = []
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             centroids.append((x + w/2, y + h/2))
#             widths.append(w)
#             heights.append(h)
#         centroids = np.array(centroids)

#         # Use centroids' x and y coordinates for clustering
#         xs = centroids[:, 0]
#         ys = centroids[:, 1]
        
#         # Use the median of the block sizes as a dynamic threshold
#         median_size = np.median(np.concatenate((np.array(widths), np.array(heights))))
#         thresh_val = median_size / 2.0

#         # Cluster x and y coordinates separately
#         x_clusters = cluster_coords(xs, thresh_val)
#         y_clusters = cluster_coords(ys, thresh_val)
        
#         num_cols = len(x_clusters)
#         num_rows = len(y_clusters)
        
#         # Initialize the grid
#         grid = np.zeros((num_rows, num_cols), dtype=int)
        
#         # Assign each contour (via its centroid) to the nearest cluster center
#         for cx, cy in centroids:
#             col = np.argmin(np.abs(np.array(x_clusters) - cx))
#             row = np.argmin(np.abs(np.array(y_clusters) - cy))
#             grid[row, col] = 1
        
#         # Optionally, save a debug visualization showing detected bounding boxes and centroids
#         debug_img = img.copy()
#         for c in contours:
#             x, y, w, h = cv2.boundingRect(c)
#             cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
#             # Draw the centroid
#             cx, cy = int(x+w/2), int(y+h/2)
#             cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
#         cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

#         detected_shapes[filename] = grid.tolist()

#     return detected_shapes

# Example usage:
# image_directory = "/mnt/data/"
# detected_shapes_output = detect_blocks_final_v3(image_directory)
# print(detected_shapes_output)




# debugging











def cluster_coords(coords, threshold):
    """
    Group sorted coordinate values into clusters where successive values
    differ by no more than the threshold. Returns the cluster centers.
    """
    coords_sorted = np.sort(coords)
    clusters = []
    current_cluster = [coords_sorted[0]]
    for coord in coords_sorted[1:]:
        if abs(coord - current_cluster[-1]) <= threshold:
            current_cluster.append(coord)
        else:
            clusters.append(np.mean(current_cluster))
            current_cluster = [coord]
    clusters.append(np.mean(current_cluster))
    return clusters




def detect_blocks_final_v2(directory):
    detected_shapes = {}
    debug_dir = os.path.join(directory, "debug")
    os.makedirs(debug_dir, exist_ok=True)

    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    for filename in filenames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {filename}. Skipping.")
            continue

        # Check for purple color using HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Convert your original values to OpenCV's HSV ranges:
        h = 263.8 / 2  # → ~131.9
        s = 58 * 2.55  # → ~148
        v = 82 * 2.55  # → ~209

        # With tolerance ranges:
        lower_purple = np.array([h-5, s-20, v-30])  # [127, 128, 179]
        upper_purple = np.array([h+5, s+20, v+30])  # [137, 168, 239]

        # Round to integers:
        lower_purple = np.array([125, 140, 190], dtype=np.uint8)
        upper_purple = np.array([140, 200, 220], dtype=np.uint8)
        mask = cv2.inRange(hsv, lower_purple, upper_purple)
        has_purple = cv2.countNonZero(mask) > 0

                # After creating the mask:
        # purple_debug = cv2.bitwise_and(img, img, mask=mask)
        # cv2.imwrite(os.path.join(debug_dir, f"purple_{filename}"), purple_debug)

        # Set kernel size based on purple presence
        kernel_size = (3, 3) if has_purple else (2, 2)
        kernel = np.ones(kernel_size, np.uint8)

        # Preprocess image: grayscale and threshold
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        _, thresh = cv2.threshold(gray, 128, 255, cv2.THRESH_BINARY)

        # Apply morphological operations
        closed = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
        eroded = cv2.erode(closed, kernel, iterations=1)

        # Find contours of the blocks
        contours, _ = cv2.findContours(eroded, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if not contours:
            detected_shapes[filename] = []
            continue

        # Compute centroids for each detected contour
        centroids = []
        widths = []
        heights = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            centroids.append((x + w/2, y + h/2))
            widths.append(w)
            heights.append(h)
        centroids = np.array(centroids)

        # Use centroids' coordinates for clustering
        xs = centroids[:, 0]
        ys = centroids[:, 1]
        
        # Dynamic threshold based on median block size
        median_size = np.median(np.concatenate((widths, heights)))
        thresh_val = median_size / 2.0

        # Cluster coordinates
        x_clusters = cluster_coords(xs, thresh_val)
        y_clusters = cluster_coords(ys, thresh_val)
        
        # Initialize grid
        num_cols = len(x_clusters)
        num_rows = len(y_clusters)
        grid = np.zeros((num_rows, num_cols), dtype=int)
        
        # Populate grid
        for cx, cy in centroids:
            col = np.argmin(np.abs(np.array(x_clusters) - cx))
            row = np.argmin(np.abs(np.array(y_clusters) - cy))
            grid[row, col] = 1

        # Save debug visualization
        debug_img = img.copy()
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            cv2.rectangle(debug_img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cx, cy = int(x+w/2), int(y+h/2)
            cv2.circle(debug_img, (cx, cy), 3, (0, 0, 255), -1)
        cv2.imwrite(os.path.join(debug_dir, f"debug_{filename}"), debug_img)

        detected_shapes[filename] = grid.tolist()

    return detected_shapes

# Example usage:
# image_directory = "/mnt/data/"
# detected_shapes_output = detect_blocks_final_v2(image_directory)
# print(detected_shapes_output)











# -----------------------------------------------------



@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    cropped_board_path, board_coords = crop_board(file_path)
    
    if not cropped_board_path or board_coords is None:
        return JSONResponse(content={"error": "Board detection failed"}, status_code=400)

    board_matrix = process_image(cropped_board_path)
    cropped_shapes_path = crop_shapes(file_path, board_coords)
    shapes_matrices = detect_shapes(cropped_shapes_path)
    # processed_shapes = process_shapes(shapes_matrices["shapes"])
    # processed_cropped_shapes = process_cropped_shapes(SHAPES_DIR)
    processed_cropped_shapes = detect_blocks_final_v2(SHAPES_DIR)
   


    for name, arr in processed_cropped_shapes.items():
        print(f"{name} =>")
        for row in arr:
            print(row)
        print()


    return {
    
        "board_matrix": board_matrix,
        "shapes": shapes_matrices,
        # "processed_shapes": processed_shapes,
        "process_cropped_shapes": processed_cropped_shapes
    }





    # resolve color detection issue
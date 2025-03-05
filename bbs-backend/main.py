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





def process_cropped_shapes(directory):
    """
    Processes each .jpg image in 'directory' and returns a dictionary where:
      - keys are image filenames (e.g., "shape_0.jpg")
      - values are 2D arrays (lists of lists) representing the shape,
        using a "block size" strategy for wide images.
    """
    results = {}
    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    
    for filename in filenames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {filename}. Skipping.")
            continue

        # Convert to HSV for background masking
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # 1) Threshold out the background (tweak these values as needed)
        lower_bg = np.array([200, 50, 40], dtype=np.uint8)
        upper_bg = np.array([240, 100, 100], dtype=np.uint8)
        bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
        mask = cv2.bitwise_not(bg_mask)  # Foreground (blocks) are white

        # 2) Find bounding box of the shape (all non-zero pixels)
        coords = cv2.findNonZero(mask)
        if coords is None:
            print(f"No blocks detected in {filename}.")
            continue

        x, y, w, h = cv2.boundingRect(coords)
        aspect_ratio = w / float(h) if h > 0 else 0
        print(f"{filename}: BoundingRect => x={x}, y={y}, w={w}, h={h}, Aspect Ratio = {aspect_ratio:.2f}")

        # Crop the ROI for further analysis
        roi = mask[y:y+h, x:x+w]

        # 3) Use block size strategy if the ROI is wide (i.e. likely 5 blocks in a row)
        # Lowered threshold from 4.0 to 3.0 based on your image characteristics.
        if aspect_ratio >= 3.0:
            print(f"{filename}: Using detect_5_blocks_in_a_row strategy.")
            shape_array = detect_5_blocks_in_a_row(roi, w, h)
            results[filename] = shape_array.tolist()
        else:
            print(f"{filename}: Using fallback_detect_blocks strategy.")
            shape_array = fallback_detect_blocks(roi)
            results[filename] = shape_array.tolist()

    return results

def detect_5_blocks_in_a_row(roi, w, h):
    """
    Given an ROI (mask) that we suspect is 5 blocks wide in a single row,
    slice the ROI horizontally into 5 segments. For each segment, if more than 20%
    of its pixels are foreground, mark it as 1.
    """
    # Create a 1x5 grid
    shape_array = np.zeros((1, 5), dtype=int)
    block_width = w // 5  # integer division for block width
    
    for i in range(5):
        x_start = i * block_width
        # For the last block, go to the full width to catch any remainder.
        x_end = (i + 1) * block_width if i < 4 else w
        cell = roi[:, x_start:x_end]
        # Mark as 1 if >20% of the cell's pixels are foreground
        if cv2.countNonZero(cell) > 0.2 * cell.size:
            shape_array[0, i] = 1

    return shape_array

def fallback_detect_blocks(roi):
    """
    A simple fallback for shapes that aren't wide enough to be recognized
    as a row of 5 blocks. This example simply returns a 1x1 grid with a 1 if
    any foreground is detected.
    """
    if cv2.countNonZero(roi) > 0:
        return np.array([[1]])
    else:
        return np.array([[0]])














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
    processed_cropped_shapes = process_cropped_shapes(SHAPES_DIR)
   
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
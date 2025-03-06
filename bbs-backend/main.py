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




# ----------- works with simple row shaped images --------

# def process_cropped_shapes(directory):
    """
    Processes each .jpg image in 'directory' and returns a dictionary of:
      {
        "filename.jpg": <2D list (grid) of 0/1 for each detected block>
      }
    Uses:
      1) HSV background removal
      2) Canny edges to highlight boundaries
      3) Distance transform + Watershed
      4) Centroid detection + row clustering
    """
    results = {}
    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])
    
    for filename in filenames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {filename}. Skipping.")
            continue

        # -- STEP 1: Remove background (HSV threshold) --
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_bg = np.array([200, 50, 40], dtype=np.uint8)
        upper_bg = np.array([240, 100, 100], dtype=np.uint8)
        bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)  # background in white
        mask = cv2.bitwise_not(bg_mask)                 # blocks in white

        # If the mask is empty, skip
        if cv2.countNonZero(mask) == 0:
            print(f"No foreground found in {filename}.")
            continue

        # Morphological opening to remove small noise
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # -- STEP 2: Canny edge detection to highlight internal boundaries --
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # Adjust these thresholds as needed:
        edges = cv2.Canny(gray, threshold1=50, threshold2=150)
        # Keep edges only within the shape (mask)
        edges_in_shape = cv2.bitwise_and(edges, mask)

        # Optionally dilate the edges to make them thicker
        edges_in_shape = cv2.dilate(edges_in_shape, kernel, iterations=1)

        # Combine edges with mask so edges become "holes" or boundaries in the shape
        # We invert edges_in_shape so edges become black (0) within the shape
        edges_inv = cv2.bitwise_not(edges_in_shape)
        # Now the shape interior is white except for black lines where edges are
        combined = cv2.bitwise_and(mask, edges_inv)

        # -- STEP 3: Distance transform + Watershed on combined result --
        dist = cv2.distanceTransform(combined, cv2.DIST_L2, 5)
        # Tweak the factor (0.5, 0.6, 0.7) to separate blocks more or less
        dist_thresh = 0.6 * dist.max()
        _, sure_fg = cv2.threshold(dist, dist_thresh, 255, 0)
        sure_fg = np.uint8(sure_fg)

        # sure_bg by dilating the original mask
        sure_bg = cv2.dilate(mask, kernel, iterations=3)
        unknown = cv2.subtract(sure_bg, sure_fg)

        # Markers for watershed
        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0

        # Run watershed
        markers = cv2.watershed(img, markers)

        # -- STEP 4: Find centroids of each labeled block --
        block_centroids = []
        unique_labels = np.unique(markers)
        for label in unique_labels:
            # Skip background (label <= 1) and boundary (-1)
            if label <= 1:
                continue

            label_mask = np.uint8(markers == label)
            contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue
            cnt = max(contours, key=cv2.contourArea)
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                block_centroids.append((cx, cy))

        if not block_centroids:
            print(f"No blocks detected after watershed in {filename}.")
            continue

        # -- STEP 5: Cluster centroids by row to build a grid --
        block_centroids.sort(key=lambda p: p[1])  # sort by y
        row_thresh = 20  # vertical tolerance for grouping into rows
        row_clusters = []
        for pt in block_centroids:
            placed = False
            for cluster in row_clusters:
                avg_y = np.mean([p[1] for p in cluster])
                if abs(pt[1] - avg_y) < row_thresh:
                    cluster.append(pt)
                    placed = True
                    break
            if not placed:
                row_clusters.append([pt])

        # Sort each row cluster by x
        for cluster in row_clusters:
            cluster.sort(key=lambda p: p[0])

        n_rows = len(row_clusters)
        n_cols = max(len(c) for c in row_clusters)
        grid = [[0]*n_cols for _ in range(n_rows)]
        for i, cluster in enumerate(row_clusters):
            for j, pt in enumerate(cluster):
                grid[i][j] = 1

        results[filename] = grid

    return results





def process_cropped_shapes(directory):
    """
    Processes each .jpg image in 'directory' and returns a dictionary:
      {
        "filename.jpg": <2D list (grid) of 0/1>
      }

    Steps:
      1) Remove background (HSV).
      2) Canny + Watershed to separate blocks if possible (for L/T shapes, etc.).
      3) If watershed => multiple blocks, cluster them into a grid.
      4) If watershed => only 1 block, fallback to best-fit line (2..5 blocks)
         either horizontally or vertically, with a penalty for unused segments.
    """
    results = {}
    filenames = sorted([f for f in os.listdir(directory) if f.endswith(".jpg")])

    for filename in filenames:
        img_path = os.path.join(directory, filename)
        img = cv2.imread(img_path)
        if img is None:
            print(f"Failed to load {filename}. Skipping.")
            continue

        # --- STEP 1: Background Removal (HSV) ---
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        lower_bg = np.array([200, 50, 40], dtype=np.uint8)
        upper_bg = np.array([240, 100, 100], dtype=np.uint8)
        bg_mask = cv2.inRange(hsv, lower_bg, upper_bg)
        mask = cv2.bitwise_not(bg_mask)  # blocks = white, background = black

        if cv2.countNonZero(mask) == 0:
            print(f"No foreground found in {filename}.")
            continue

        # Morphological open to reduce noise
        kernel = np.ones((3, 3), np.uint8)
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

        # Find bounding box for fallback usage
        coords = cv2.findNonZero(mask)
        x, y, w, h = cv2.boundingRect(coords)
        aspect_ratio = (w / float(h)) if h else 0

        # --- STEP 2: Canny edges to highlight internal boundaries ---
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray, 50, 150)
        edges_in_shape = cv2.bitwise_and(edges, mask)
        edges_in_shape = cv2.dilate(edges_in_shape, kernel, iterations=1)
        edges_inv = cv2.bitwise_not(edges_in_shape)
        combined = cv2.bitwise_and(mask, edges_inv)

        # --- STEP 3: Watershed ---
        dist = cv2.distanceTransform(combined, cv2.DIST_L2, 5)
        dist_thresh = 0.6 * dist.max()
        _, sure_fg = cv2.threshold(dist, dist_thresh, 255, 0)
        sure_fg = np.uint8(sure_fg)

        sure_bg = cv2.dilate(mask, kernel, iterations=3)
        unknown = cv2.subtract(sure_bg, sure_fg)

        _, markers = cv2.connectedComponents(sure_fg)
        markers = markers + 1
        markers[unknown == 255] = 0
        markers = cv2.watershed(img, markers)

        # Gather block info from watershed
        blocks_info = []
        unique_labels = np.unique(markers)
        for label in unique_labels:
            # Skip background (<=1) and boundary (-1)
            if label <= 1:
                continue
            label_mask = (markers == label).astype(np.uint8)
            contours, _ = cv2.findContours(label_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            if not contours:
                continue
            cnt = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(cnt)
            if area > 0:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    blocks_info.append((label, area, (cx, cy)))

        num_blocks = len(blocks_info)

        if num_blocks > 1:
            # Multiple blocks => cluster them into a grid
            shape_grid = cluster_blocks_into_grid(blocks_info)
            results[filename] = shape_grid
        else:
            # Only 0 or 1 block => fallback best-fit line
            shape_grid = fallback_best_fit_line(mask, x, y, w, h, aspect_ratio)
            results[filename] = shape_grid.tolist()

    return results


def cluster_blocks_into_grid(blocks_info, row_thresh=20):
    """
    Given a list of (label, area, (cx, cy)), cluster them into rows
    and build a 2D grid with 1's for blocks.
    """
    # Sort by y
    blocks_info.sort(key=lambda b: b[2][1])
    row_clusters = []
    for lbl, area, (cx, cy) in blocks_info:
        placed = False
        for cluster in row_clusters:
            avg_y = np.mean([p[2][1] for p in cluster])
            if abs(cy - avg_y) < row_thresh:
                cluster.append((lbl, area, (cx, cy)))
                placed = True
                break
        if not placed:
            row_clusters.append([(lbl, area, (cx, cy))])

    # Sort each row by x
    for cluster in row_clusters:
        cluster.sort(key=lambda b: b[2][0])

    n_rows = len(row_clusters)
    n_cols = max(len(c) for c in row_clusters)
    grid = [[0]*n_cols for _ in range(n_rows)]
    for i, cluster in enumerate(row_clusters):
        for j, (lbl, area, (cx, cy)) in enumerate(cluster):
            grid[i][j] = 1
    return grid


def fallback_best_fit_line(full_mask, x, y, w, h, aspect_ratio):
    """
    If watershed merges everything into 1 block, we guess a single row or column.
    - If aspect_ratio >= 1.5 => horizontal line
    - else => vertical line
    We try n from 2..5 blocks, compute a "score" = coverage_ratio - penalty_for_unused_segments.
    The penalty avoids over-segmentation for shapes that only have 3 or 4 blocks.
    """
    roi = full_mask[y:y+h, x:x+w]
    total_fg = cv2.countNonZero(roi)
    if total_fg == 0:
        # No foreground => just return a single block
        return np.array([[0]])
    
    best_score = -9999
    best_grid = np.array([[1]])  # fallback if nothing better
    # We won't do n=1 in the loop because we already know we have at least 1 block.
    # We'll do 2..5. If you might have 6 or 7 blocks, expand the range.
    
    if aspect_ratio >= 1.5:
        # Horizontal line
        for n in range(2, 6):
            grid_1xn = np.zeros((1, n), dtype=int)
            seg_w = w // n
            coverage_count = 0
            filled_count = 0
            for i in range(n):
                x_start = i * seg_w
                x_end = (i+1)*seg_w if i < (n-1) else w
                cell = roi[:, x_start:x_end]
                c_nonzero = cv2.countNonZero(cell)
                # Mark cell as 1 if >20% filled
                if c_nonzero > 0.2 * cell.size:
                    grid_1xn[0, i] = 1
                    coverage_count += c_nonzero
                    filled_count += 1
            
            coverage_ratio = coverage_count / float(total_fg)
            # Penalty: subtract 0.1 for each unused segment
            # so if we fill 3 segments out of 5, penalty = 0.2
            penalty = 0.1 * (n - filled_count)
            score = coverage_ratio - penalty
            
            if score > best_score:
                best_score = score
                best_grid = grid_1xn
    else:
        # Vertical line
        for n in range(2, 6):
            grid_nx1 = np.zeros((n, 1), dtype=int)
            seg_h = h // n
            coverage_count = 0
            filled_count = 0
            for i in range(n):
                y_start = i*seg_h
                y_end = (i+1)*seg_h if i < (n-1) else h
                cell = roi[y_start:y_end, :]
                c_nonzero = cv2.countNonZero(cell)
                if c_nonzero > 0.2 * cell.size:
                    grid_nx1[i, 0] = 1
                    coverage_count += c_nonzero
                    filled_count += 1
            
            coverage_ratio = coverage_count / float(total_fg)
            penalty = 0.1 * (n - filled_count)
            score = coverage_ratio - penalty
            
            if score > best_score:
                best_score = score
                best_grid = grid_nx1

    # If we never improved over the default, best_grid remains.
    return best_grid














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